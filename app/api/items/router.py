from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import Context, get_context
from app.api.filters import get_filters
from app.api.sort import get_sort_entities
from app.api.utils import PaginatedResponseDTO, get_search
from app.domain.items.commands import (
    create_item_command,
    delete_item_command,
    get_item_command,
    get_items_command,
    update_item_command,
)
from app.domain.items.entities import Item, ItemCreate, ItemUpdate
from cleanstack.entities import EntityId, FilterEntity, Pagination, SortEntity

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=PaginatedResponseDTO[Item])
def get_items(
    context: Annotated[Context, Depends(get_context)],
    search: Annotated[str | None, Depends(get_search)],
    filters: Annotated[list[FilterEntity], Depends(get_filters)],
    sort: Annotated[list[SortEntity], Depends(get_sort_entities)],
    pagination: Annotated[Pagination, Depends()],
) -> Any:
    return get_items_command(
        context,
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


@router.get("/{item_id}")
def get_item(
    context: Annotated[Context, Depends(get_context)],
    item_id: EntityId,
) -> Any:
    return get_item_command(context, item_id=item_id)


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    context: Annotated[Context, Depends(get_context)],
    data: ItemCreate,
) -> Any:
    return create_item_command(context, data=data)


@router.patch("/{item_id}", response_model=Item)
def update_item(
    context: Annotated[Context, Depends(get_context)],
    item_id: EntityId,
    data: ItemUpdate,
) -> Any:
    return update_item_command(context, item_id=item_id, data=data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    context: Annotated[Context, Depends(get_context)],
    item_id: EntityId,
) -> None:
    delete_item_command(context, item_id=item_id)
