import sqlalchemy
from sqlalchemy.orm import Session

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


class SyncSQLRepository[T: DomainEntity, OrmT: OrmEntity](SQLMixin[T, OrmT]):
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
            load_options=self._load_options,
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
            items=[self._to_domain_entity(item) for item in data_result],
        )

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        stmt = (
            sqlalchemy.select(self.orm_model_type)
            .where(self.orm_model_type.id == entity_id)
            .options(*self._load_options)
        )
        result = self.session.execute(stmt)
        db_entity = result.scalar_one_or_none()
        return self._to_domain_entity(db_entity) if db_entity else None

    def create(self, entity: T, /) -> T:
        values = self._to_database_values(entity)
        stmt = sqlalchemy.insert(self.orm_model_type).values(**values)
        self.session.execute(stmt)
        self._create_relations(entity)
        return entity

    def update(self, entity: T, /) -> T:
        values = self._to_database_values(entity, exclude={"id"})
        stmt = (
            sqlalchemy.update(self.orm_model_type)
            .where(self.orm_model_type.id == entity.id)
            .values(**values)
        )
        self.session.execute(stmt)
        self._update_relations(entity)
        return entity

    def delete(self, entity: T) -> None:
        self._delete_relations(entity)
        stmt = sqlalchemy.delete(self.orm_model_type).where(
            self.orm_model_type.id == entity.id
        )
        self.session.execute(stmt)

    def _create_relations(self, entity: T, /) -> None:
        pass

    def _update_relations(self, entity: T, /) -> None:
        pass

    def _delete_relations(self, entity: T, /) -> None:
        pass
