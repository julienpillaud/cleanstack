from collections.abc import Iterator

import pytest

from app.core.settings import RepositoryType, Settings
from app.infrastructure.mongo.utils import MongoResource
from app.infrastructure.sql.utils import SQLResource
from tests.factories.containers import ContainerMongoFactory, ContainerSQLFactory
from tests.factories.items import ItemMongoFactory, ItemSQLFactory

type ItemFactory = ItemMongoFactory | ItemSQLFactory
type ContainerFactory = ContainerMongoFactory | ContainerSQLFactory
type Resource = MongoResource | SQLResource


@pytest.fixture(scope="session")
def init_resource(settings: Settings) -> Iterator[Resource]:
    resource: Resource

    match settings.repository_type:
        case RepositoryType.MONGO:
            resource = MongoResource.from_settings(settings)
        case RepositoryType.SQL:
            resource = SQLResource.from_settings(settings)
            resource.create_all()

    yield resource

    resource.release()


@pytest.fixture
def db_resource(init_resource: Resource) -> Iterator[Resource]:
    yield init_resource

    init_resource.reset()
