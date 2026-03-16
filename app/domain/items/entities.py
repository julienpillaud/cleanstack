import uuid
from enum import StrEnum

from app.domain.entities import DateTime
from app.domain.tags.entities import Tag
from cleanstack.entities import DomainEntity


class ItemStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Item(DomainEntity):
    uuid_field: uuid.UUID
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    datetime_field: DateTime
    strenum_field: ItemStatus
    optional_field: str | None
    tags: list[Tag]
