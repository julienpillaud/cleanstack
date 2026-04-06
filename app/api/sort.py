import re
from typing import Annotated

from fastapi import HTTPException, Query, status

from cleanstack.entities import SortEntity, SortOrder

DIRECTIONS = "|".join(value for value in SortOrder)
SORT_PATTERN = re.compile(
    r"^([a-zA-Z0-9_]+)"  # Start with the field
    r"\["
    rf"({DIRECTIONS})"
    r"]"
)


def parse_sort_entities(sort_entities: list[str], /) -> list[SortEntity]:
    entities = []
    for sort_entity in sort_entities:
        match = SORT_PATTERN.match(sort_entity)
        if not match:
            raise ValueError("Invalid sort format")

        field, order = match.groups()
        entities.append(
            SortEntity(
                field=field,
                order=SortOrder(order),
            )
        )

    return entities


def get_sort_entities(
    sort_entities: Annotated[
        list[str] | None,
        Query(alias="sort"),
    ] = None,
) -> list[SortEntity]:
    if not sort_entities:
        return []

    try:
        return parse_sort_entities(sort_entities)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid sort format",
        ) from error
