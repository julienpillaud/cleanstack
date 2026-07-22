from app.domain.items.entities import Item
from app.infrastructure.sql.tables import OrmItem
from cleanstack.sql.asynchronous.repository import AsyncSQLRepository


class ItemSQLRepository(AsyncSQLRepository[Item, OrmItem]):
    domain_entity_type = Item
    orm_model_type = OrmItem
    searchable_fields = ("string_field",)
