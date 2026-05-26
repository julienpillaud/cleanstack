from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.containers.entities import Container
from app.infrastructure.sql.tables import OrmContainer, OrmNode
from cleanstack.infrastructure.sql.base import SQLMixin
from cleanstack.infrastructure.sql.synchronous.repository import SyncSQLRepository


class ContainerSQLMixin(SQLMixin[Container, OrmContainer]):
    domain_entity_type = Container
    orm_model_type = OrmContainer

    def to_orm_entity(self, entity: Container) -> OrmContainer:
        return OrmContainer(
            id=entity.id,
            name=entity.name,
            nodes=[OrmNode(id=node.id, label=node.label) for node in entity.nodes],
        )

    @property
    def load_options(self) -> list[ExecutableOption]:
        # SELECT * FROM node WHERE container_id IN (...);
        return [selectinload(OrmContainer.nodes)]


class SyncContainerSQLRepository(
    ContainerSQLMixin,
    SyncSQLRepository[Container, OrmContainer],
):
    pass
