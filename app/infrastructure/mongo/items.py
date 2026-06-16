from app.domain.items.entities import Item
from cleanstack.mongo import AsyncMongoRepository, SyncMongoRepository


class SyncItemMongoRepository(SyncMongoRepository[Item]):
    domain_entity_type = Item
    collection_name = "items"
    searchable_fields = ("string_field",)


class AsyncItemMongoRepository(AsyncMongoRepository[Item]):
    domain_entity_type = Item
    collection_name = "items"
    searchable_fields = ("string_field",)
