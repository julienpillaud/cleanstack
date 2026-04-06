from app.domain.items.entities import Item
from app.infrastructure.sql.tables import OrmItem
from cleanstack.infrastructure.sql.asynchronous.repository import AsyncSQLRepository
from cleanstack.infrastructure.sql.base import SQLMixin
from cleanstack.infrastructure.sql.synchronous.repository import SyncSQLRepository


class ItemSQLMixin(SQLMixin[Item, OrmItem]):
    domain_entity_type = Item
    orm_model_type = OrmItem
    searchable_fields = ("string_field",)


class SyncItemSQLRepository(ItemSQLMixin, SyncSQLRepository[Item, OrmItem]):
    pass


class AsyncItemSQLRepository(ItemSQLMixin, AsyncSQLRepository[Item, OrmItem]):
    pass
