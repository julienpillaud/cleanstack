from typing import Any

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, ColumnElement, Select, String, func, or_, select
from sqlalchemy.sql.base import ExecutableOption

from app.infrastructure.sql.logger import logger
from cleanstack import FilterEntity, Pagination, SortEntity, SortOrder
from cleanstack.entities import BaseEntity
from cleanstack.exceptions import InvalidFilterError
from cleanstack.sql.entities import OrmEntity
from cleanstack.sql.utils import apply_operator, get_filter_metadata
from cleanstack.utils import convert_filter_value_generic


class Statement[OrmT: OrmEntity](BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: Select[tuple[OrmT]]
    count: Select[tuple[int]]


class SQLMixin[T: BaseEntity, OrmT: OrmEntity]:
    domain_entity_type: type[T]
    orm_model_type: type[OrmT]
    searchable_fields: tuple[str, ...] = ()

    def to_domain_entity(self, orm_entity: OrmT, /) -> T:
        return self.domain_entity_type.model_validate(orm_entity)

    def to_database_entity(self, entity: T, /) -> OrmEntity:
        return self.orm_model_type(**entity.model_dump())

    @property
    def load_options(self) -> list[ExecutableOption]:
        return []

    def search_clause(self, search: str | None, /) -> ColumnElement[bool] | None:
        if not search or not self.searchable_fields:
            return None

        columns: dict[str, Column[String]] = {}
        for name, column in self.orm_model_type.columns_map().items():
            if name not in self.searchable_fields:
                continue

            if not isinstance(column.type, String):
                logger.warning(
                    f"Non String Column '{name}' ignored from search ({column.type})"
                )
                continue

            columns[name] = column

        conditions = [field.ilike(f"%{search}%") for field in columns.values()]
        return or_(*conditions)

    def filters_clauses(
        self,
        filters: list[FilterEntity] | None,
        /,
    ) -> list[ColumnElement[bool]] | None:
        if not filters:
            return None

        clauses: list[ColumnElement[bool]] = []
        for filter_entity in filters:
            column = self._get_field(filter_entity.field)
            metadata = get_filter_metadata(column)
            value = convert_filter_value_generic(
                filter_entity=filter_entity,
                metadata=metadata,
            )
            clause = apply_operator(
                value=value,
                column=column,
                operator=filter_entity.operator,
            )
            clauses.append(clause)

        return clauses

    def sort_clauses(
        self,
        sort: list[SortEntity] | None = None,
        /,
    ) -> list[ColumnElement[bool]] | None:
        if not sort:
            return None

        clauses: list[ColumnElement[bool]] = []
        for sort_entity in sort:
            column = self._get_field(sort_entity.field)
            clause = (
                column.desc() if sort_entity.order == SortOrder.DESC else column.asc()
            )
            clauses.append(clause)

        return clauses

    def build_statement(
        self,
        *,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination,
    ) -> Statement[OrmT]:
        stmt = select(self.orm_model_type).options(*self.load_options)

        _search_clause = self.search_clause(search)
        if _search_clause is not None:
            stmt = stmt.where(_search_clause)

        _filters_clauses = self.filters_clauses(filters)
        if _filters_clauses is not None:
            for clause in _filters_clauses:
                stmt = stmt.where(clause)

        count_stmt = select(func.count()).select_from(stmt.subquery())

        _sort_clauses = self.sort_clauses(sort)
        if _sort_clauses is not None:
            for clause in _sort_clauses:
                stmt = stmt.order_by(clause)

        stmt = stmt.offset(pagination.skip).limit(pagination.size)

        return Statement(data=stmt, count=count_stmt)

    def _get_field(self, field: str, /) -> Column[Any]:
        columns = self.orm_model_type.columns_map()
        column = columns.get(field)
        if column is None:
            raise InvalidFilterError("Unauthorized field")

        return column
