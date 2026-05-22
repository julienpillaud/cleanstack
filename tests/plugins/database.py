from collections.abc import Iterator
from typing import Protocol

import pytest

from app.core.settings import RepositoryType, Settings
from app.infrastructure.mongo.utils import create_mongo_resource
from app.infrastructure.sql.utils import create_sql_resource
from cleanstack.infrastructure.sql.entities import OrmEntity
from tests.factories.containers import ContainerMongoFactory, ContainerSQLFactory
from tests.factories.items import ItemMongoFactory, ItemSQLFactory

type ItemFactory = ItemMongoFactory | ItemSQLFactory
type ContainerFactory = ContainerMongoFactory | ContainerSQLFactory


class ResourceProtocol(Protocol):
    def release(self) -> None: ...

    def reset(self) -> None: ...


@pytest.fixture(scope="session")
def init_resource(settings: Settings) -> Iterator[ResourceProtocol]:
    resource: ResourceProtocol

    match settings.repository_type:
        case RepositoryType.MONGO:
            resource = create_mongo_resource(settings=settings)
        case RepositoryType.SQL:
            resource = create_sql_resource(settings=settings)
            OrmEntity.metadata.drop_all(resource.engine)
            OrmEntity.metadata.create_all(resource.engine)

    yield resource

    resource.release()


@pytest.fixture
def db_resource(init_resource: ResourceProtocol) -> Iterator[ResourceProtocol]:
    yield init_resource

    init_resource.reset()
