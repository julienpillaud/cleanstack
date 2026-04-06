from cleanstack.entities import DomainEntity
from cleanstack.infrastructure.mongo.types import MongoDocument
from cleanstack.infrastructure.mongo.utils import normalize_ids


class MongoRepositoryError(Exception):
    pass


class MongoMixin[T: DomainEntity]:
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...] = ()

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: T, /) -> MongoDocument:
        """Convert a domain entity to a MongoDB document to be saved to the database.

        Can be overridden to take into account relationships.
        """
        # Use the entity's id as the document's _id
        # Don't let mongo generate an ObjectId for us
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document

    @property
    def _lookup(self) -> list[MongoDocument]:
        return []
