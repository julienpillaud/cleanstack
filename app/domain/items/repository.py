from enum import StrEnum
from typing import Protocol

from app.domain.items.entities import Item
from cleanstack.domain import RepositoryProtocol


class RepositoryType(StrEnum):
    RELATIONAL = "relational"
    DOCUMENT = "document"


class ItemRepositoryProtocol(RepositoryProtocol[Item], Protocol): ...
