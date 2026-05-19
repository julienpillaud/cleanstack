import uuid
from typing import Any

from app.domain.containers.entities import Container
from app.domain.nodes.entities import Node
from app.infrastructure.mongo.containers import SyncContainerMongoRepository
from app.infrastructure.sql.containers import SyncContainerSQLRepository
from cleanstack.factories.mongo import BaseMongoFactory
from cleanstack.factories.sql import BaseSQLFactory
from tests.factories.utils import faker


def generate_nodes(labels: list[str] | None = None, /) -> list[Node]:
    labels = labels or [
        faker.random_string() for _ in range(faker.random_int(max_value=10))
    ]
    return [Node(id=uuid.uuid7(), label=label) for label in labels]


def generate_container(**kwargs: Any) -> Container:
    return Container(
        id=kwargs.get("id", uuid.uuid7()),
        name=kwargs.get("name", faker.random_string()),
        nodes=generate_nodes(kwargs.get("nodes")),
    )


class ContainerMongoFactory(BaseMongoFactory[Container]):
    def build(self, **kwargs: Any) -> Container:
        return generate_container(**kwargs)

    @property
    def _repository(self) -> SyncContainerMongoRepository:
        return SyncContainerMongoRepository(database=self.database)


class ContainerSQLFactory(BaseSQLFactory[Container]):
    def build(self, **kwargs: Any) -> Container:
        return generate_container(**kwargs)

    @property
    def _repository(self) -> SyncContainerSQLRepository:
        return SyncContainerSQLRepository(session=self.session)
