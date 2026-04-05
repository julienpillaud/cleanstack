from enum import StrEnum
from typing import Protocol

from app.domain.items.entities import Item
from cleanstack.domain.repository import AsyncRepositoryProtocol, SyncRepositoryProtocol


class RepositoryType(StrEnum):
    RELATIONAL = "relational"
    DOCUMENT = "document"


class SyncItemRepositoryProtocol(SyncRepositoryProtocol[Item], Protocol): ...


class AsyncItemRepositoryProtocol(AsyncRepositoryProtocol[Item], Protocol): ...
