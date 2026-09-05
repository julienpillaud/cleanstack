from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.domain.containers.entities import Container
from app.domain.containers.repository import ContainerRepositoryProtocol
from cleanstack import EntityId
from cleanstack.mongo import AsyncMongoRepository, MongoDocument


class ContainerMongoRepository(ContainerRepositoryProtocol):
    domain_entity_type = Container
    collection_name = "containers"
    searchable_fields = ()

    def __init__(
        self,
        database: AsyncDatabase[MongoDocument],
        session: AsyncClientSession | None = None,
    ) -> None:
        self.repository = AsyncMongoRepository[Container].from_spec(
            binding=self,
            database=database,
            session=session,
        )

    async def get_by_id(self, entity_id: EntityId, /) -> Container | None:
        return await self.repository.get_by_id(entity_id)

    async def save(self, entity: Container, /) -> None:
        await self.repository.save(entity)

    async def update(self, entity: Container, /) -> None:
        await self.repository.update(entity)

    async def remove(self, entity: Container, /) -> None:
        await self.repository.remove(entity)
