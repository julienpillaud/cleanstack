from typing import Protocol

from cleanstack.entities.base import DomainEntity, EntityId
from cleanstack.entities.filters import FilterEntity
from cleanstack.entities.pagination import PaginatedResponse, Pagination
from cleanstack.entities.sort import SortEntity


class SyncRepositoryProtocol[T: DomainEntity](Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    def save(self, entity: T, /) -> None: ...

    def update(self, entity: T, /) -> None: ...

    def remove(self, entity: T, /) -> None: ...


class AsyncRepositoryProtocol[T: DomainEntity](Protocol):
    async def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    async def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    async def save(self, entity: T, /) -> None: ...

    async def update(self, entity: T, /) -> None: ...

    async def remove(self, entity: T, /) -> None: ...
