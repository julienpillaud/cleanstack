from pydantic import BaseModel
from pydantic.fields import ComputedFieldInfo, FieldInfo

from cleanstack import FilterEntity, Pagination, SortEntity, SortOrder
from cleanstack.entities import BaseEntity
from cleanstack.exceptions import InvalidFieldError
from cleanstack.mongo.types import MongoDocument
from cleanstack.mongo.utils import (
    apply_operator,
    convert_field_name,
    get_filter_metadata,
    normalize_ids,
)
from cleanstack.utils import convert_filter_value_generic


class Pipeline(BaseModel):
    data: list[MongoDocument]
    count: list[MongoDocument]


class MongoMixin[T: BaseEntity]:
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...] = ()

    def to_domain_entity(self, document: MongoDocument, /) -> T:
        normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def to_database_entity(entity: T, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document

    @property
    def lookup(self) -> list[MongoDocument]:
        return []

    def search_stage(self, search: str | None) -> list[MongoDocument]:
        if not search:
            return []

        search_pipeline = [
            {field: {"$regex": search.strip(), "$options": "i"}}
            for field in self.searchable_fields
        ]
        return [{"$match": {"$or": search_pipeline}}]

    def filters_stage(self, filters: list[FilterEntity] | None) -> list[MongoDocument]:
        if not filters:
            return []

        filters_pipeline = {}
        for filter_entity in filters:
            field_info = self._get_field(filter_entity.field)
            metadata = get_filter_metadata(field_info)
            value = convert_filter_value_generic(
                filter_entity=filter_entity,
                metadata=metadata,
            )
            condition = apply_operator(value=value, operator=filter_entity.operator)
            field_name = convert_field_name(filter_entity.field)
            filters_pipeline[field_name] = condition

        return [{"$match": filters_pipeline}]

    def sort_stage(self, sort: list[SortEntity] | None) -> list[MongoDocument]:
        if not sort:
            return []

        order_map = {SortOrder.ASC: 1, SortOrder.DESC: -1}
        sort_pipeline = {}
        for sort_entity in sort:
            # Check if the field exists in the model
            self._get_field(sort_entity.field)

            sort_pipeline[sort_entity.field] = order_map[sort_entity.order]

        return [{"$sort": sort_pipeline}]

    def _build_pipeline(
        self,
        *,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination,
    ) -> Pipeline:
        base = [
            *self.search_stage(search),
            *self.filters_stage(filters),
        ]
        return Pipeline(
            data=[
                *base,
                *self.lookup,
                *self.sort_stage(sort),
                {"$skip": pagination.skip},
                {"$limit": pagination.size},
            ],
            count=[*base, {"$count": "total"}],
        )

    def _get_field(self, field: str, /) -> FieldInfo | ComputedFieldInfo:
        field_info = self.domain_entity_type.model_fields.get(field)
        if field_info:
            return field_info

        computed_field_info = self.domain_entity_type.model_computed_fields.get(field)
        if computed_field_info:
            return computed_field_info

        raise InvalidFieldError("Invalid field")
