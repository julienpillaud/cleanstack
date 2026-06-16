import sqlalchemy
from sqlalchemy.orm import Session

from cleanstack.entities import (
    BaseEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.sql.builder import StatementBuilder
from cleanstack.sql.entities import OrmEntity
from cleanstack.sql.mixin import SQLMixin


class SyncSQLRepository[T: BaseEntity, OrmT: OrmEntity](SQLMixin[T, OrmT]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(
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
            load_options=self.load_options,
        ).apply(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

        total = self.session.scalar(statement.count) or 0
        data_result = self.session.scalars(statement.data)

        return PaginatedResponse(
            page=pagination.page,
            size=pagination.size,
            pages=pagination.pages(total),
            total=total,
            items=[self.to_domain_entity(item) for item in data_result],
        )

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        stmt = (
            sqlalchemy.select(self.orm_model_type)
            .where(self.orm_model_type.id == entity_id)
            .options(*self.load_options)
        )
        result = self.session.execute(stmt)
        db_entity = result.scalar_one_or_none()
        return self.to_domain_entity(db_entity) if db_entity else None

    def save(self, entity: T, /) -> None:
        orm_entity = self.to_orm_entity(entity)
        self.session.add(orm_entity)

    def update(self, entity: T, /) -> None:
        orm_entity = self.to_orm_entity(entity)
        self.session.merge(orm_entity)

    def remove(self, entity: T) -> None:
        orm_entity = self.session.get(self.orm_model_type, entity.id)
        self.session.delete(orm_entity)
