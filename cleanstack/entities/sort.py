from enum import StrEnum

from pydantic import BaseModel


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class SortEntity(BaseModel):
    field: str
    order: SortOrder = SortOrder.ASC
