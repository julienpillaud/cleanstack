import datetime
import uuid
from collections.abc import Iterator
from typing import Any, TypeAliasType, Union, get_args, get_origin

from pydantic.fields import FieldInfo

from cleanstack.entities import (
    FilterOperator,
)
from cleanstack.infrastructure.exceptions import InvalidFilterError
from cleanstack.infrastructure.mongo.types import MongoDocument
from cleanstack.infrastructure.utils import FilterMetadata


def iter_dicts(value: dict[Any, Any]) -> Iterator[dict[Any, Any]]:
    stack: list[Any] = [value]

    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            yield node
            stack.extend(node.values())

        elif isinstance(node, list):
            stack.extend(node)


def normalize_ids(document: MongoDocument) -> None:
    for d in iter_dicts(document):
        if "_id" in d:
            d["id"] = str(d.pop("_id"))


def convert_field_name(field: str) -> str:
    return "_id" if field == "id" else field


CONVERTERS: dict[type[Any], Any] = {
    bool: lambda value: value == "true",
    datetime.datetime: datetime.datetime.fromisoformat,
    float: float,
    int: int,
    str: str,
    uuid.UUID: uuid.UUID,
}


def resolve_annotation(field_info: FieldInfo) -> Any:
    annotation = field_info.annotation
    if not annotation:
        raise InvalidFilterError("Unsupported type")

    # Case : type EntityId = uuid.UUID
    if isinstance(annotation, TypeAliasType):
        return annotation.__value__

    # Case: str | None
    if get_origin(annotation) is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(args) != 1:
            raise InvalidFilterError("Multiple union types are not supported")

        return args[0]

    # Case : primitive subclasses
    if isinstance(annotation, type):
        if issubclass(annotation, bool):
            return bool
        if issubclass(annotation, str):
            return str
        if issubclass(annotation, int):
            return int
        if issubclass(annotation, float):
            return float

    return annotation


def get_filter_metadata(field_info: FieldInfo, /) -> FilterMetadata:
    resolved_type = resolve_annotation(field_info)
    converter = CONVERTERS.get(resolved_type)
    if not converter:
        raise InvalidFilterError("Unsupported type")

    return FilterMetadata(
        is_discrete=resolved_type in {uuid.UUID, str},
        is_boolean=resolved_type is bool,
        converter=converter,
    )


def apply_operator(value: Any, operator: FilterOperator) -> MongoDocument:
    match operator:
        case FilterOperator.EQ:
            return {"$eq": value}
        case FilterOperator.GT:
            return {"$gt": value}
        case FilterOperator.LT:
            return {"$lt": value}
        case FilterOperator.GTE:
            return {"$gte": value}
        case FilterOperator.LTE:
            return {"$lte": value}
        case FilterOperator.IN:
            return {"$in": value}
        case FilterOperator.NIN:
            return {"$nin": value}
