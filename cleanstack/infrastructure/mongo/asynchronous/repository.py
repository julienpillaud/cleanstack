from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from cleanstack.entities import (
    DomainEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.infrastructure.mongo.base import MongoMixin, MongoRepositoryError
from cleanstack.infrastructure.mongo.builder import PipelineBuilder
from cleanstack.infrastructure.mongo.types import MongoDocument


class AsyncMongoRepository[T: DomainEntity](MongoMixin[T]):
    def __init__(
        self,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ) -> None:
        self.collection = database[self.collection_name]
        self.session = session

    async def get_all(
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

        count_cursor = await self.collection.aggregate(
            pipeline=pipeline.count,
            session=self.session,
        )
        count_result = await count_cursor.try_next()
        total = count_result["total"] if count_result else 0
        data_cursor = await self.collection.aggregate(
            pipeline=pipeline.data,
            session=self.session,
        )
        items = await data_cursor.to_list()

        return PaginatedResponse(
            page=pagination.page,
            size=pagination.size,
            pages=pagination.pages(total),
            total=total,
            items=[self._to_domain_entity(item) for item in items],
        )

    async def get_by_id(self, entity_id: EntityId, /) -> T | None:
        pipeline = [{"$match": {"_id": entity_id}}]
        pipeline.extend(self._lookup)

        cursor = await self.collection.aggregate(
            pipeline=pipeline,
            session=self.session,
        )
        result = await cursor.try_next()

        return self._to_domain_entity(result) if result else None

    async def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = await self.collection.insert_one(
            document=db_entity,
            session=self.session,
        )
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entity")

        return entity

    async def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = await self.collection.replace_one(
            filter={"_id": entity.id},
            replacement=db_entity,
            session=self.session,
        )
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to update entity")

        return entity

    async def delete(self, entity: T, /) -> None:
        await self.collection.delete_one(
            filter={"_id": entity.id},
            session=self.session,
        )
