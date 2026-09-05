from typing import Protocol

from app.domain.containers.entities import Container
from cleanstack import EntityId


class ContainerRepositoryProtocol(Protocol):
    async def get_by_id(self, entity_id: EntityId, /) -> Container | None: ...

    async def save(self, entity: Container, /) -> None: ...

    async def update(self, entity: Container, /) -> None: ...

    async def remove(self, entity: Container, /) -> None: ...
