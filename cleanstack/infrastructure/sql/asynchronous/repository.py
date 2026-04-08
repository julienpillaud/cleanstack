import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from cleanstack.entities import (
    DomainEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.infrastructure.sql.base import SQLMixin
from cleanstack.infrastructure.sql.builder import StatementBuilder
from cleanstack.infrastructure.sql.entities import OrmEntity


class AsyncSQLRepository[T: DomainEntity, OrmT: OrmEntity](SQLMixin[T, OrmT]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()
        statement = StatementBuilder(
            self.orm_model_type,
            self.searchable_fields,
            load_options=self._load_options,
        ).apply(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

        total = await self.session.scalar(statement.count) or 0
        data_result = await self.session.scalars(statement.data)

        return PaginatedResponse(
            page=pagination.page,
            size=pagination.size,
            pages=pagination.pages(total),
            total=total,
            items=[self._to_domain_entity(item) for item in data_result],
        )

    async def get_by_id(self, entity_id: EntityId, /) -> T | None:
        stmt = (
            sqlalchemy.select(self.orm_model_type)
            .where(self.orm_model_type.id == entity_id)
            .options(*self._load_options)
        )
        result = await self.session.execute(stmt)
        db_entity = result.scalar_one_or_none()
        return self._to_domain_entity(db_entity) if db_entity else None

    async def create(self, entity: T, /) -> T:
        values = self._to_database_values(entity)
        stmt = sqlalchemy.insert(self.orm_model_type).values(**values)
        await self.session.execute(stmt)
        await self._create_relations(entity)
        return entity

    async def update(self, entity: T, /) -> T:
        values = self._to_database_values(entity, exclude={"id"})
        stmt = (
            sqlalchemy.update(self.orm_model_type)
            .where(self.orm_model_type.id == entity.id)
            .values(**values)
        )
        await self.session.execute(stmt)
        await self._update_relations(entity)
        return entity

    async def delete(self, entity: T) -> None:
        await self._delete_relations(entity)
        stmt = sqlalchemy.delete(self.orm_model_type).where(
            self.orm_model_type.id == entity.id
        )
        await self.session.execute(stmt)

    async def _create_relations(self, entity: T, /) -> None:
        pass

    async def _update_relations(self, entity: T, /) -> None:
        pass

    async def _delete_relations(self, entity: T, /) -> None:
        pass
