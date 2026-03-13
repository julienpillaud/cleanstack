from pymongo.client_session import ClientSession
from pymongo.database import Database

from cleanstack.domain import RepositoryProtocol
from cleanstack.entities import (
    DomainEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.infrastructure.mongo.builder import PipelineBuilder
from cleanstack.infrastructure.mongo.types import MongoDocument
from cleanstack.infrastructure.mongo.utils import normalize_ids


class MongoRepositoryError(Exception):
    pass


class MongoRepository[T: DomainEntity](RepositoryProtocol[T]):
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...] = ()

    def __init__(
        self,
        database: Database[MongoDocument],
        session: ClientSession | None = None,
    ):
        self.database = database
        self.collection = self.database[self.collection_name]
        self.session = session

    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()

        pipeline = PipelineBuilder(
            self.domain_entity_type,
            self.searchable_fields,
            lookup=self._lookup,
        ).apply(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

        count_cursor = self.collection.aggregate(
            pipeline=pipeline.count,
            session=self.session,
        )
        count_result = count_cursor.try_next()
        total = count_result["total"] if count_result else 0

        data_cursor = self.collection.aggregate(
            pipeline=pipeline.data,
            session=self.session,
        )

        return PaginatedResponse(
            page=pagination.page,
            size=pagination.size,
            pages=pagination.pages(total),
            total=total,
            items=[self._to_domain_entity(item) for item in data_cursor],
        )

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        pipeline = [{"$match": {"_id": entity_id}}]
        pipeline.extend(self._lookup)
        cursor = self.collection.aggregate(
            pipeline=pipeline,
            session=self.session,
        )
        result = cursor.try_next()
        return self._to_domain_entity(result) if result else None

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.insert_one(
            document=db_entity,
            session=self.session,
        )
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entity")

        return entity

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.replace_one(
            filter={"_id": entity.id},
            replacement=db_entity,
            session=self.session,
        )
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to update entity")

        return entity

    def delete(self, entity: T, /) -> None:
        self.collection.delete_one(
            filter={"_id": entity.id},
            session=self.session,
        )

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: T, /) -> MongoDocument:
        """Convert a domain entity to a MongoDB document to be saved to the database.

        Can be overridden to take into account relationships.
        """
        # Use the entity's id as the document's _id
        # Don't let mongo generate an ObjectId for us
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document

    @property
    def _lookup(self) -> list[MongoDocument]:
        return []
