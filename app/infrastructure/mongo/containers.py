from app.domain.containers.entities import Container
from cleanstack.mongo import AsyncMongoRepository


class ContainerMongoRepository(AsyncMongoRepository[Container]):
    domain_entity_type = Container
    collection_name = "containers"
