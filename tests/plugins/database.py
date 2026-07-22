from collections.abc import AsyncIterator

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
async def init_resource(settings: Settings) -> AsyncIterator[Resource]:
    resource: Resource

    match settings.repository_type:
        case RepositoryType.MONGO:
            resource = await MongoResource.from_settings(settings)
        case RepositoryType.SQL:
            resource = await SQLResource.from_settings(settings)
            await resource.init()

    yield resource

    await resource.release()


@pytest.fixture
async def db_resource(init_resource: Resource) -> AsyncIterator[Resource]:
    yield init_resource

    await init_resource.reset()
