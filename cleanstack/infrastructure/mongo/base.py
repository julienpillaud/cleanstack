from cleanstack.entities import DomainEntity
from cleanstack.infrastructure.mongo.types import MongoDocument
from cleanstack.infrastructure.mongo.utils import normalize_ids


class MongoRepositoryError(Exception):
    pass


class MongoMixin[T: DomainEntity]:
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...] = ()

    def to_domain_entity(self, document: MongoDocument, /) -> T:
        normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def to_database_entity(entity: T, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document

    @property
    def lookup(self) -> list[MongoDocument]:
        return []
