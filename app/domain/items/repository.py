from typing import Protocol

from app.domain.items.entities import Item
from cleanstack.domain.repository import AsyncRepositoryProtocol, SyncRepositoryProtocol


class SyncItemRepositoryProtocol(SyncRepositoryProtocol[Item], Protocol): ...


class AsyncItemRepositoryProtocol(AsyncRepositoryProtocol[Item], Protocol): ...
