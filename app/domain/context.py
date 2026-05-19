from typing import Protocol

from app.domain.containers.repository import SyncContainerRepositoryProtocol
from app.domain.items.repository import SyncItemRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def item_repository(self) -> SyncItemRepositoryProtocol: ...

    @property
    def container_repository(self) -> SyncContainerRepositoryProtocol: ...
