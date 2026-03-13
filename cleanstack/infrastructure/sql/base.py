from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.base import ExecutableOption

from cleanstack.domain import RepositoryProtocol
from cleanstack.entities import (
    DomainEntity,
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from cleanstack.infrastructure.sql.builder import StatementBuilder
from cleanstack.infrastructure.sql.entities import OrmEntity


class SQLRepositoryError(Exception):
    pass


class SQLRepository[T: DomainEntity, OrmT: OrmEntity](
    RepositoryProtocol[T],
):
    domain_entity_type: type[T]
    orm_model_type: type[OrmT]
    searchable_fields: tuple[str, ...] = ()

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
        db_result = self._get_orm_entity(entity_id)
        return self._to_domain_entity(db_result) if db_result else None

    def create(self, entity: T, /) -> T:
        orm_entity = self._to_database_entity(entity)
        self.session.add(orm_entity)
        return entity

    def update(self, entity: T, /) -> T:
        db_entity = self._get_orm_entity(entity.id)
        if not db_entity:
            raise SQLRepositoryError("Failed to update entity")

        for key, value in entity.model_dump(exclude={"id"}).items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)

        return entity

    def delete(self, entity: T) -> None:
        stmt = delete(self.orm_model_type).where(self.orm_model_type.id == entity.id)
        self.session.execute(stmt)

    def _get_orm_entity(self, entity_id: EntityId, /) -> OrmT | None:
        stmt = select(self.orm_model_type).where(self.orm_model_type.id == entity_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def _to_domain_entity(self, orm_entity: OrmT, /) -> T:
        return self.domain_entity_type.model_validate(orm_entity)

    def _to_database_entity(self, entity: T, /) -> OrmT:
        """Convert a domain entity to an ORM entity to be saved to the database.

        Can be overridden to take into account relationships.
        """
        return self.orm_model_type(**entity.model_dump())

    @property
    def _load_options(self) -> list[ExecutableOption]:
        return []
