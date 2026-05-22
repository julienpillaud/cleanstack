import pytest

from app.infrastructure.mongo.utils import MongoResource
from app.infrastructure.sql.utils import SQLResource
from tests.factories.containers import ContainerMongoFactory, ContainerSQLFactory
from tests.factories.items import ItemMongoFactory, ItemSQLFactory
from tests.plugins.database import ContainerFactory, ItemFactory, ResourceProtocol


class Factory:
    def __init__(self, items: ItemFactory, containers: ContainerFactory) -> None:
        self.items = items
        self.containers = containers

    @classmethod
    def from_mongo_resource(cls, resource: MongoResource) -> Factory:
        return cls(
            items=ItemMongoFactory(database=resource.database),
            containers=ContainerMongoFactory(database=resource.database),
        )

    @classmethod
    def from_sql_resource(cls, resource: SQLResource) -> Factory:
        return cls(
            items=ItemSQLFactory(session_factory=resource.session_factory),
            containers=ContainerSQLFactory(session_factory=resource.session_factory),
        )


@pytest.fixture
def factory(db_resource: ResourceProtocol) -> Factory:
    match db_resource:
        case MongoResource():
            return Factory.from_mongo_resource(db_resource)
        case SQLResource():
            return Factory.from_sql_resource(db_resource)
        case _:
            raise RuntimeError()
