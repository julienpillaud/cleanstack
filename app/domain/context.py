from typing import Protocol

from app.domain.containers.repository import ContainerRepositoryProtocol
from app.domain.items.repository import ItemRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def item_repository(self) -> ItemRepositoryProtocol: ...

    @property
    def container_repository(self) -> ContainerRepositoryProtocol: ...
