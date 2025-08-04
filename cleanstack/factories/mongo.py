from typing import Generic, TypeVar

try:
    from pymongo.collection import Collection
except ImportError as e:
    raise RuntimeError(
        'To use MongoDB utilities, you need to install "cleanstack[mongo]"'
    ) from e

from cleanstack.entities import DomainModel
from cleanstack.factories.base import BaseFactory
from cleanstack.infrastructure.mongo.entities import MongoDocument

T = TypeVar("T", bound=DomainModel)


class MongoBaseFactory(BaseFactory[T], Generic[T]):
    def __init__(self, collection: Collection[MongoDocument]):
        self.collection = collection

    def _insert_one(self, entity: T) -> None:
        db_entity = self._to_database_entity(entity)
        self.collection.insert_one(db_entity)

    def _to_database_entity(self, entity: T, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document
