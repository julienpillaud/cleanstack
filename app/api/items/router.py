from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.utils import PaginatedResponseDTO
from app.dependencies.fastapi.dependencies import (
    get_domain,
    get_filters,
    get_search,
    get_sort_entities,
)
from app.domain.domain import Domain
from app.domain.items.entities import Item
from app.domain.items.repository import RepositoryType
from cleanstack.entities import EntityId, FilterEntity, Pagination, SortEntity

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=PaginatedResponseDTO[Item])
def get_items(
    domain: Annotated[Domain, Depends(get_domain)],
    repository: RepositoryType,
    search: Annotated[str | None, Depends(get_search)],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    pagination: Annotated[Pagination, Depends()],
) -> Any:
    return domain.get_items(
        repository=repository,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get("/{item_id}")
def get_item(
    domain: Annotated[Domain, Depends(get_domain)],
    repository: RepositoryType,
    item_id: EntityId,
) -> Any:
    return domain.get_item(repository=repository, item_id=item_id)
