from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.tables import OrmItem
from cleanstack import EntityId, FilterEntity, PaginatedResponse, Pagination, SortEntity
from cleanstack.sql.asynchronous.repository import AsyncSQLRepository


class ItemSQLRepository(ItemRepositoryProtocol):
    domain_entity_type = Item
    orm_model_type = OrmItem
    searchable_fields = ("string_field",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = AsyncSQLRepository[Item, OrmItem].from_spec(
            binding=self,
            session=session,
        )

    async def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Item]:
        return await self.repository.get_all(
            search=search,
            filters=filters,
            sort=sort,
            pagination=pagination,
        )

    async def get_by_id(self, entity_id: EntityId, /) -> Item | None:
        return await self.repository.get_by_id(entity_id)

    async def save(self, entity: Item, /) -> None:
        await self.repository.save(entity)

    async def update(self, entity: Item, /) -> None:
        await self.repository.update(entity)

    async def remove(self, entity: Item, /) -> None:
        await self.repository.remove(entity)
