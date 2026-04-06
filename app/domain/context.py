from typing import Protocol

from app.domain.items.repository import SyncItemRepositoryProtocol
from cleanstack.domain import BaseContextProtocol


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def item_repository(self) -> SyncItemRepositoryProtocol: ...
