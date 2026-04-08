from pydantic import BaseModel

from app.domain.nodes.entities import Node
from cleanstack.entities import DomainEntity


class Container(DomainEntity):
    name: str
    nodes: list[Node]  # One-to-many relationship


class ContainerCreate(BaseModel):
    name: str
    nodes: list[str]


class ContainerUpdate(BaseModel):
    name: str | None = None
    nodes: list[str] | None = None
