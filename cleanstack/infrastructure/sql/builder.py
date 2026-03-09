from typing import Any, Self

from sqlalchemy import Column, Select, func, or_, select

from cleanstack.entities import FilterEntity, Pagination, SortEntity, SortOrder
from cleanstack.infrastructure.exceptions import InvalidFilterError
from cleanstack.infrastructure.sql.entities import OrmEntity
from cleanstack.infrastructure.sql.utils import apply_operator, get_filter_metadata
from cleanstack.infrastructure.utils import convert_filter_value_generic


class StatementBuilder[T: OrmEntity]:
    def __init__(
        self,
        orm_model_type: type[T],
        searchable_fields: tuple[str, ...],
    ) -> None:
        self.orm_model_type = orm_model_type
        self.searchable_fields = searchable_fields

        self._stmt = select(self.orm_model_type)
        self._count_stmt = self._get_count_stmt()

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
        self._count_stmt = self._get_count_stmt()
        self._apply_sort(sort)
        self._apply_pagination(pagination)
        return self

    @property
    def count(self) -> Select[tuple[int]]:
        return self._count_stmt

    @property
    def data(self) -> Select[tuple[T]]:
        return self._stmt

    def _get_field(self, field: str, /) -> Column[Any]:
        columns = self.orm_model_type.columns_map()
        column = columns.get(field)
        if column is None:
            raise InvalidFilterError("Unauthorized field")

        return column

    def _get_count_stmt(self) -> Select[tuple[int]]:
        return select(func.count()).select_from(self._stmt.subquery())

    def _apply_search(self, search: str | None, /) -> None:
        if not search:
            return

        columns = {
            name: column
            for name, column in self.orm_model_type.columns_map().items()
            if name in self.searchable_fields
        }
        conditions = [field.ilike(f"%{search}%") for field in columns.values()]
        self._stmt = self._stmt.where(or_(*conditions))

    def _apply_filters(self, filters: list[FilterEntity] | None, /) -> None:
        if not filters:
            return

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
            self._stmt = self._stmt.where(clause)

    def _apply_sort(self, sort: list[SortEntity] | None = None, /) -> None:
        if not sort:
            return

        for sort_entity in sort:
            column = self._get_field(sort_entity.field)
            clause = (
                column.desc() if sort_entity.order == SortOrder.DESC else column.asc()
            )
            self._stmt = self._stmt.order_by(clause)

    def _apply_pagination(self, pagination: Pagination, /) -> None:
        self._stmt = self._stmt.offset(pagination.skip).limit(pagination.size)
