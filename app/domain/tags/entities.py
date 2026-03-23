from pydantic import BaseModel

from cleanstack.entities import DomainEntity


class Tag(DomainEntity):
    name: str


class TagCreate(BaseModel):
    name: str
