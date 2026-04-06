import pytest

from cleanstack.infrastructure.mongo.uow import MongoConfig
from cleanstack.infrastructure.sql.uow import SQLConfig
from tests.factories.items import ItemMongoFactory, ItemSQLFactory

type ItemFactory = ItemMongoFactory | ItemSQLFactory


@pytest.fixture
def item_factory(
    repo_config: MongoConfig | SQLConfig,
) -> ItemFactory:
    if isinstance(repo_config, MongoConfig):
        return ItemMongoFactory(config=repo_config)

    if isinstance(repo_config, SQLConfig):
        return ItemSQLFactory(context=repo_config)

    raise RuntimeError()
