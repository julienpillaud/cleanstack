from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from cleanstack.infrastructure.mongo.base import MongoRepository


class ItemMongoRepository(MongoRepository[Item], ItemRepositoryProtocol):
    domain_entity_type = Item
    collection_name = "items"
    searchable_fields = ("string_field",)
