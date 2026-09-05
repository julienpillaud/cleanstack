from typing import Protocol

from app.domain.items.entities import Item
from cleanstack import EntityId, FilterEntity, PaginatedResponse, Pagination, SortEntity


class ItemRepositoryProtocol(Protocol):
    async def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Item]: ...

    async def get_by_id(self, entity_id: EntityId, /) -> Item | None: ...

    async def save(self, entity: Item, /) -> None: ...

    async def update(self, entity: Item, /) -> None: ...

    async def remove(self, entity: Item, /) -> None: ...
