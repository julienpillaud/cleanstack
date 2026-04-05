import pytest

from cleanstack.infrastructure.mongo.uow import MongoContext
from cleanstack.infrastructure.sql.uow import SQLContext
from tests.factories.items import ItemFactory, ItemMongoFactory, ItemSQLFactory


@pytest.fixture
def item_mongo_factory(mongo_context: MongoContext) -> ItemMongoFactory:
    return ItemMongoFactory(context=mongo_context)


@pytest.fixture
def item_sql_factory(sql_context: SQLContext) -> ItemSQLFactory:
    return ItemSQLFactory(context=sql_context)


@pytest.fixture
def item_factory(
    item_mongo_factory: ItemMongoFactory,
    item_sql_factory: ItemSQLFactory,
) -> ItemFactory:
    return ItemFactory(
        mongo_factory=item_mongo_factory,
        sql_factory=item_sql_factory,
    )
