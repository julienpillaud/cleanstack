from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from cleanstack.infrastructure.mongo.base import MongoRepository
from cleanstack.infrastructure.mongo.types import MongoDocument


class ItemMongoRepository(MongoRepository[Item], ItemRepositoryProtocol):
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
