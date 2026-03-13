from app.domain.tags.entities import Tag
from app.domain.tags.repository import TagRepositoryProtocol
from cleanstack.infrastructure.mongo.base import MongoRepository


class TagMongoRepository(MongoRepository[Tag], TagRepositoryProtocol):
    domain_entity_type = Tag
    collection_name = "tags"
