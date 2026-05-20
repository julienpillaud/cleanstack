import sqlalchemy
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.containers.entities import Container
from app.infrastructure.sql.tables import OrmContainer, OrmNode
from cleanstack.infrastructure.sql.base import SQLMixin
from cleanstack.infrastructure.sql.synchronous.repository import SyncSQLRepository


class ContainerSQLMixin(SQLMixin[Container, OrmContainer]):
    domain_entity_type = Container
    orm_model_type = OrmContainer

    @property
    def load_options(self) -> list[ExecutableOption]:
        # SELECT * FROM node WHERE container_id IN (...);
        return [selectinload(OrmContainer.nodes)]

    @staticmethod
    def extra_excluded_fields() -> set[str]:
        return {"nodes"}


class SyncContainerSQLRepository(
    ContainerSQLMixin,
    SyncSQLRepository[Container, OrmContainer],
):
    def _create_relations(self, entity: Container, /) -> None:
        if not entity.nodes:
            return

        # INSERT INTO node (...) VALUES (...);
        self._insert_nodes(entity)

    def _update_relations(self, entity: Container, /) -> None:
        # DELETE FROM node WHERE container_id = :id;
        stmt = sqlalchemy.delete(OrmNode).where(OrmNode.container_id == entity.id)
        self.session.execute(stmt)

        if not entity.nodes:
            return

        # INSERT INTO node (...) VALUES (...);
        self._insert_nodes(entity)

    def _delete_relations(self, entity: Container, /) -> None:
        # DELETE FROM node WHERE container_id = :id;
        stmt = sqlalchemy.delete(OrmNode).where(OrmNode.container_id == entity.id)
        self.session.execute(stmt)

    def _insert_nodes(self, entity: Container, /) -> None:
        stmt = sqlalchemy.insert(OrmNode).values(
            [
                {"id": node.id, "label": node.label, "container_id": entity.id}
                for node in entity.nodes
            ]
        )
        self.session.execute(stmt)
