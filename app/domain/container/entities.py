import uuid

from app.domain.tags.entities import Tag
from cleanstack.entities import DomainEntity


class Container(DomainEntity):
    name: str
    tags: list[Tag]
    item_id: uuid.UUID
