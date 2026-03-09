import re

from cleanstack.entities import FilterEntity, FilterOperator

SEPARATOR = "="
OPERATORS = "|".join(value for value in FilterOperator if value != FilterOperator.EQ)
FILTER_PATTERN = re.compile(
    r"^([a-zA-Z0-9_]+)"  # Start with the field
    r"(?:\["  # Optional operator surrounded by brackets
    rf"({OPERATORS})"
    r"])?"
    rf"{SEPARATOR}"
    r"([a-zA-Z0-9_,.:-]+)$"  # End with the value
)


def parse_filters(filters: list[str], /) -> list[FilterEntity]:
    entities = []
    for filter_entity in filters:
        match = FILTER_PATTERN.match(filter_entity)
        if not match:
            raise ValueError("Invalid filter format")

        field, operator_str, value_part = match.groups()
        operator = FilterOperator(operator_str) if operator_str else FilterOperator.EQ

        if operator in (FilterOperator.IN, FilterOperator.NIN):
            value = value_part.split(",")
            if "" in value:
                raise ValueError("Invalid filter format")
        else:
            if "," in value_part:
                raise ValueError("Invalid filter format")
            value = value_part

        entities.append(
            FilterEntity(
                field=field,
                value=value,
                operator=operator,
            )
        )

    return entities
