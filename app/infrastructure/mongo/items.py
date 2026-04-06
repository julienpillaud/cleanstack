from app.domain.items.entities import Item
from cleanstack.infrastructure.mongo import (
    AsyncMongoRepository,
    MongoMixin,
    SyncMongoRepository,
)


class ItemMongoMixin(MongoMixin[Item]):
    domain_entity_type = Item
    collection_name = "items"
    searchable_fields = ("string_field",)


class SyncItemMongoRepository(ItemMongoMixin, SyncMongoRepository[Item]):
    pass


class AsyncItemMongoRepository(ItemMongoMixin, AsyncMongoRepository[Item]):
    pass
