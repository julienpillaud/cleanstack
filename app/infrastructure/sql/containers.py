from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.containers.entities import Container
from app.domain.containers.repository import ContainerRepositoryProtocol
from app.infrastructure.sql.tables import OrmContainer, OrmNode
from cleanstack import EntityId
from cleanstack.sql import AsyncSQLRepository


class ContainerSQLAdapter(AsyncSQLRepository[Container, OrmContainer]):
    def to_database_entity(self, entity: Container) -> OrmContainer:
        return OrmContainer(
            id=entity.id,
            name=entity.name,
            nodes=[OrmNode(id=node.id, label=node.label) for node in entity.nodes],
        )

    @property
    def load_options(self) -> list[ExecutableOption]:
        # SELECT * FROM node WHERE container_id IN (...);
        return [selectinload(OrmContainer.nodes)]


class ContainerSQLRepository(ContainerRepositoryProtocol):
    domain_entity_type = Container
    orm_model_type = OrmContainer
    searchable_fields = ()

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = ContainerSQLAdapter.from_binding(
            binding=self,
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
