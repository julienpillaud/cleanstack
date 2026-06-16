import uuid
from enum import StrEnum

from pydantic import BaseModel, computed_field

from app.domain.entities import DateTime
from cleanstack import BaseEntity


class ItemStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Item(BaseEntity):
    uuid_field: uuid.UUID
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    datetime_field: DateTime
    strenum_field: ItemStatus
    optional_field: ItemStatus | None

    @computed_field
    def computed_field(self) -> float:
        return self.float_field * 2


class ItemCreate(BaseModel):
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    strenum_field: ItemStatus
    optional_field: ItemStatus | None


class ItemUpdate(BaseModel):
    string_field: str | None = None
    int_field: int | None = None
    float_field: float | None = None
    bool_field: bool | None = None
    strenum_field: ItemStatus | None = None
    optional_field: ItemStatus | None = None
