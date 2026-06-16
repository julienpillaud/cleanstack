import datetime
import uuid
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    ColumnElement,
    DateTime,
    Float,
    Integer,
    String,
    Uuid,
)

from cleanstack.entities import (
    FilterOperator,
)
from cleanstack.exceptions import InvalidFilterError
from cleanstack.utils import FilterMetadata

CONVERTERS: dict[type[Any], Any] = {
    Boolean: lambda value: value == "true",
    DateTime: datetime.datetime.fromisoformat,
    Float: float,
    Integer: int,
    String: str,
    Uuid: uuid.UUID,
}


def get_filter_metadata(column: Column[Any]) -> FilterMetadata:
    converter = None
    for column_type, func in CONVERTERS.items():
        if isinstance(column.type, column_type):
            converter = func
            break

    if not converter:
        raise InvalidFilterError("Unsupported type")

    return FilterMetadata(
        is_discrete=isinstance(column.type, (Uuid, String)),
        is_boolean=isinstance(column.type, Boolean),
        converter=converter,
    )


def apply_operator(
    value: Any,
    operator: FilterOperator,
    column: Column[Any],
) -> ColumnElement[bool]:
    match operator:
        case FilterOperator.EQ:
            return column == value  # type: ignore[no-any-return]
        case FilterOperator.GT:
            return column > value  # type: ignore[no-any-return]
        case FilterOperator.LT:
            return column < value  # type: ignore[no-any-return]
        case FilterOperator.GTE:
            return column >= value  # type: ignore[no-any-return]
        case FilterOperator.LTE:
            return column <= value  # type: ignore[no-any-return]
        case FilterOperator.IN:
            return column.in_(value)
        case FilterOperator.NIN:
            return column.notin_(value)
