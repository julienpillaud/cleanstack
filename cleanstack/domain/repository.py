from typing import Protocol

from cleanstack.entities.base import DomainEntity, EntityId
from cleanstack.entities.filters import FilterEntity
from cleanstack.entities.pagination import PaginatedResponse, Pagination
from cleanstack.entities.sort import SortEntity


class RepositoryProtocol[T: DomainEntity](Protocol):
    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    def create(self, entity: T, /) -> T: ...

    def update(self, entity: T, /) -> T: ...

    def delete(self, entity: T, /) -> None: ...
