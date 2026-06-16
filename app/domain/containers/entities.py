from pydantic import BaseModel

from app.domain.nodes.entities import Node
from cleanstack import BaseEntity


class Container(BaseEntity):
    name: str
    nodes: list[Node]  # One-to-many relationship


class ContainerCreate(BaseModel):
    name: str
    nodes: list[str]


class ContainerUpdate(BaseModel):
    name: str | None = None
    nodes: list[str] | None = None
