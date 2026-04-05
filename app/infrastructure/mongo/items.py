from app.domain.items.entities import Item
from cleanstack.infrastructure.mongo import (
    AsyncMongoRepository,
    MongoDocument,
    MongoRepositoryMixin,
    SyncMongoRepository,
)


class ItemMongoRepositoryMixin(MongoRepositoryMixin[Item]):
    domain_entity_type = Item
    collection_name = "items"
    searchable_fields = ("string_field",)

    @staticmethod
    def _to_database_entity(entity: Item, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id", "tags"})
        document["_id"] = entity.id
        document["tag_ids"] = [tag.id for tag in entity.tags]
        return document

    @property
    def _lookup(self) -> list[MongoDocument]:
        return [
            {
                "$lookup": {
                    "from": "tags",
                    "localField": "tag_ids",
                    "foreignField": "_id",
                    "as": "tags",
                }
            }
        ]


class SyncItemMongoRepository(ItemMongoRepositoryMixin, SyncMongoRepository[Item]):
    pass


class AsyncItemMongoRepository(ItemMongoRepositoryMixin, AsyncMongoRepository[Item]):
    pass
