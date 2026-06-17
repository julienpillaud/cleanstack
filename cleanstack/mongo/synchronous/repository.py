from pymongo.synchronous.client_session import ClientSession
from pymongo.synchronous.database import Database

from cleanstack.entities import (
    BaseEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.mongo.mixin import MongoMixin
from cleanstack.mongo.types import MongoDocument


class SyncMongoRepository[T: BaseEntity](MongoMixin[T]):
    def __init__(
        self,
        database: Database[MongoDocument],
        session: ClientSession | None = None,
    ) -> None:
        self.collection = database[self.collection_name]
        self.session = session

    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()
        pipeline = self._build_pipeline(
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
        items = data_cursor.to_list()

        return PaginatedResponse(
            page=pagination.page,
            size=pagination.size,
            pages=pagination.pages(total),
            total=total,
            items=[self.to_domain_entity(item) for item in items],
        )

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        pipeline = [{"$match": {"_id": entity_id}}]
        pipeline.extend(self.lookup)
        cursor = self.collection.aggregate(
            pipeline=pipeline,
            session=self.session,
        )
        result = cursor.try_next()
        return self.to_domain_entity(result) if result else None

    def save(self, entity: T, /) -> None:
        db_entity = self.to_database_entity(entity)

        self.collection.insert_one(
            document=db_entity,
            session=self.session,
        )

    def update(self, entity: T, /) -> None:
        db_entity = self.to_database_entity(entity)

        self.collection.replace_one(
            filter={"_id": entity.id},
            replacement=db_entity,
            session=self.session,
        )

    def remove(self, entity: T, /) -> None:
        self.collection.delete_one(
            filter={"_id": entity.id},
            session=self.session,
        )
