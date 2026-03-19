import uuid
from enum import StrEnum

from pydantic import computed_field

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
    optional_field: ItemStatus | None
    tags: list[Tag]

    @computed_field
    def computed_field(self) -> float:
        return self.float_field * 2
