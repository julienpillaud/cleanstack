from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from cleanstack.entities import FilterEntity, FilterOperator
from cleanstack.infrastructure.exceptions import InvalidFilterError


class FilterMetadata(BaseModel):
    is_discrete: bool
    is_boolean: bool
    converter: Callable[[Any], Any]


def convert_filter_value_generic(
    filter_entity: FilterEntity,
    metadata: FilterMetadata,
) -> Any:
    if isinstance(filter_entity.value, list):
        return [
            cast_filter_value_generic(
                value=value,
                operator=filter_entity.operator,
                metadata=metadata,
            )
            for value in filter_entity.value
        ]
    return cast_filter_value_generic(
        value=filter_entity.value,
        operator=filter_entity.operator,
        metadata=metadata,
    )


def cast_filter_value_generic(
    value: str,
    operator: FilterOperator,
    metadata: FilterMetadata,
) -> Any:
    if metadata.is_discrete and operator not in (
        FilterOperator.EQ,
        FilterOperator.IN,
        FilterOperator.NIN,
    ):
        raise InvalidFilterError("Unsupported operator")

    if metadata.is_boolean:
        if operator != FilterOperator.EQ:
            raise InvalidFilterError("Unsupported operator")
        if value not in ("true", "false"):
            raise InvalidFilterError("Invalid value format")

    try:
        return metadata.converter(value)
    except ValueError as error:
        raise InvalidFilterError("Invalid value format") from error
