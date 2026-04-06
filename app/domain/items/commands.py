import datetime
import uuid

from app.domain.context import ContextProtocol
from app.domain.items.entities import Item, ItemCreate, ItemUpdate
from cleanstack.domain import NotFoundError
from cleanstack.entities import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
)


def get_items_command(
    context: ContextProtocol,
    /,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Item]:
    return context.item_repository.get_all(
        search=search,
        filters=filters,
        sort=sort,
        pagination=pagination,
    )


def get_item_command(context: ContextProtocol, /, item_id: EntityId) -> Item:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    return item


def create_item_command(context: ContextProtocol, /, data: ItemCreate) -> Item:
    # Explicitly write all fields for clarity
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
    return context.item_repository.create(item)


def update_item_command(
    context: ContextProtocol,
    /,
    item_id: EntityId,
    data: ItemUpdate,
) -> Item:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    return context.item_repository.update(item)


def delete_item_command(context: ContextProtocol, /, item_id: EntityId) -> None:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    context.item_repository.delete(item)
