from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.tables import OrmItem, OrmTag
from cleanstack.infrastructure.sql.base import SQLRepository


class ItemSQLRepository(SQLRepository[Item, OrmItem], ItemRepositoryProtocol):
    domain_entity_type = Item
    orm_model_type = OrmItem
    searchable_fields = ("string_field",)

    def _to_database_entity(self, entity: Item, /) -> OrmItem:
        # Get tags to create the Item and fill the association table
        tag_ids = [tag.id for tag in entity.tags]
        stmt = select(OrmTag).where(OrmTag.id.in_(tag_ids))
        orm_tags = self.session.execute(stmt).scalars().all()

        data = entity.model_dump(exclude={"tags"})
        return OrmItem(**data, tags=orm_tags)

    @property
    def _load_options(self) -> list[ExecutableOption]:
        # selectinload to avoid N+1 queries
        return [selectinload(OrmItem.tags)]
