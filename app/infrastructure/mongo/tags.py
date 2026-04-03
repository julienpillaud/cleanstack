from app.domain.tags.entities import Tag
from app.domain.tags.repository import TagRepositoryProtocol
from cleanstack.infrastructure.mongo.synchronous.repository import SyncMongoRepository


class TagMongoRepository(SyncMongoRepository[Tag], TagRepositoryProtocol):
    domain_entity_type = Tag
    collection_name = "tags"
