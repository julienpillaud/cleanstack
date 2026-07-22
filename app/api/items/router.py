from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain
from app.api.filters import get_filters
from app.api.sort import get_sort_entities
from app.api.utils import PaginatedResponseDTO, get_search
from app.core.domain import Domain
from app.domain.items.entities import Item, ItemCreate, ItemUpdate
from app.domain.items.use_cases import (
    create_item,
    delete_item,
    get_item,
    get_items,
    update_item,
)
from cleanstack import EntityId, FilterEntity, PaginatedResponse, Pagination, SortEntity

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=PaginatedResponseDTO[Item])
async def get_items_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    search: Annotated[str | None, Depends(get_search)],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    pagination: Annotated[Pagination, Depends()],
) -> PaginatedResponse[Item]:
    return await domain.run(
        get_items,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get("/{item_id}")
async def get_item_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    item_id: EntityId,
) -> Item:
    return await domain.run(get_item, item_id=item_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ItemCreate,
) -> Item:
    return await domain.run(create_item, data=data)


@router.patch("/{item_id}")
async def update_item_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    item_id: EntityId,
    data: ItemUpdate,
) -> Item:
    return await domain.run(update_item, item_id=item_id, data=data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    item_id: EntityId,
) -> None:
    await domain.run(delete_item, item_id=item_id)
