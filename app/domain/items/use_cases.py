import datetime
import uuid

from app.domain.context import ContextProtocol
from app.domain.exceptions import NotFoundError
from app.domain.items.entities import Item, ItemCreate, ItemUpdate
from cleanstack import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)


async def get_items(
    context: ContextProtocol,
    /,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Item]:
    return await context.item_repository.get_all(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


async def get_item(context: ContextProtocol, /, item_id: EntityId) -> Item:
    item = await context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    return item


async def create_item(context: ContextProtocol, /, data: ItemCreate) -> Item:
    item = Item(
        id=uuid.uuid7(),
        uuid_field=uuid.uuid7(),
        string_field=data.string_field,
        int_field=data.int_field,
        float_field=data.float_field,
        bool_field=data.bool_field,
        datetime_field=datetime.datetime.now(datetime.UTC),
        strenum_field=data.strenum_field,
        optional_field=data.optional_field,
    )
    await context.item_repository.save(item)
    return item


async def update_item(
    context: ContextProtocol,
    /,
    item_id: EntityId,
    data: ItemUpdate,
) -> Item:
    item = await context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    await context.item_repository.update(item)
    return item


async def delete_item(context: ContextProtocol, /, item_id: EntityId) -> None:
    item = await context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    await context.item_repository.remove(item)
