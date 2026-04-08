from app.domain.containers.entities import Container
from cleanstack.infrastructure.mongo import MongoMixin, SyncMongoRepository


class ContainerMongoMixin(MongoMixin[Container]):
    domain_entity_type = Container
    collection_name = "containers"


class SyncContainerMongoRepository(ContainerMongoMixin, SyncMongoRepository[Container]):
    pass
