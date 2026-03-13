from app.domain.context import ContextProtocol
from app.domain.items.entities import Item
from app.domain.items.repository import RepositoryType
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
    repository: RepositoryType,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
    sort: list[SortEntity] | None = None,
    pagination: Pagination | None = None,
) -> PaginatedResponse[Item]:
    match repository:
        case RepositoryType.RELATIONAL:
            return context.item_relational_repository.get_all(
                search=search,
                filters=filters,
                sort=sort,
                pagination=pagination,
            )
        case RepositoryType.DOCUMENT:
            return context.item_document_repository.get_all(
                search=search,
                filters=filters,
                sort=sort,
                pagination=pagination,
            )


def get_item_command(
    context: ContextProtocol,
    /,
    repository: RepositoryType,
    item_id: EntityId,
) -> Item | None:
    match repository:
        case RepositoryType.RELATIONAL:
            return context.item_relational_repository.get_by_id(item_id)
        case RepositoryType.DOCUMENT:
            return context.item_document_repository.get_by_id(item_id)
