from typing import Self

from pydantic.fields import ComputedFieldInfo, FieldInfo

from cleanstack.entities import (
    DomainEntity,
    FilterEntity,
    Pagination,
    SortEntity,
    SortOrder,
)
from cleanstack.infrastructure.exceptions import InvalidFieldError
from cleanstack.infrastructure.mongo.types import MongoDocument
from cleanstack.infrastructure.mongo.utils import (
    apply_operator,
    convert_field_name,
    get_filter_metadata,
)
from cleanstack.infrastructure.utils import convert_filter_value_generic


class PipelineBuilder[T: DomainEntity]:
    def __init__(
        self,
        domain_entity_type: type[T],
        searchable_fields: tuple[str, ...],
        lookup: list[MongoDocument],
    ) -> None:
        self.domain_entity_type = domain_entity_type
        self.searchable_fields = searchable_fields
        self.lookup = lookup

        self._pipeline: list[MongoDocument] = []
        self._count_pipeline: list[MongoDocument] = [{"$count": "total"}]

    def apply(
        self,
        *,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination,
    ) -> Self:
        self._apply_search(search)
        self._apply_filters(filters)
        self._count_pipeline = [*self._pipeline, {"$count": "total"}]
        self._pipeline.extend(self.lookup)
        self._apply_sort(sort)
        self._apply_pagination(pagination)
        return self

    @property
    def count(self) -> list[MongoDocument]:
        return self._count_pipeline

    @property
    def data(self) -> list[MongoDocument]:
        return self._pipeline

    def _get_field(self, field: str, /) -> FieldInfo | ComputedFieldInfo:
        field_info = self.domain_entity_type.model_fields.get(field)
        if field_info:
            return field_info

        computed_field_info = self.domain_entity_type.model_computed_fields.get(field)
        if computed_field_info:
            return computed_field_info

        raise InvalidFieldError("Invalid field")

    def _apply_search(self, search: str | None) -> None:
        if not search:
            return

        search_pipeline = [
            {field: {"$regex": search.strip(), "$options": "i"}}
            for field in self.searchable_fields
        ]
        self._pipeline.append({"$match": {"$or": search_pipeline}})

    def _apply_filters(self, filters: list[FilterEntity] | None) -> None:
        if not filters:
            return

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

        self._pipeline.append({"$match": filters_pipeline})

    def _apply_sort(self, sort: list[SortEntity] | None) -> None:
        if not sort:
            return

        order_map = {SortOrder.ASC: 1, SortOrder.DESC: -1}
        sort_pipeline = {}
        for sort_entity in sort:
            # Check if the field exists in the model
            self._get_field(sort_entity.field)

            sort_pipeline[sort_entity.field] = order_map[sort_entity.order]

        self._pipeline.append({"$sort": sort_pipeline})

    def _apply_pagination(self, pagination: Pagination) -> None:
        self._pipeline.extend([{"$skip": pagination.skip}, {"$limit": pagination.size}])
