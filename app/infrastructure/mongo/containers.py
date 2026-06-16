from app.domain.containers.entities import Container
from cleanstack.mongo import SyncMongoRepository


class SyncContainerMongoRepository(SyncMongoRepository[Container]):
    domain_entity_type = Container
    collection_name = "containers"
