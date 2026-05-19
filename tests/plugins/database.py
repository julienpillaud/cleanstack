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


class ResourceContext(Protocol):
    def close(self) -> None: ...


class DatabaseContext(Protocol):
    def teardown(self) -> None: ...

    @property
    def item_factory(self) -> ItemFactory: ...

    @property
    def container_factory(self) -> ContainerFactory: ...


class MongoResourceContext(ResourceContext):
    def __init__(self, settings: Settings) -> None:
        self.resource = create_mongo_resource(settings=settings)
        self.client = self.resource.client
        self.database = self.resource.database

    def close(self) -> None:
        self.resource.close()


class SQLResourceContext:
    def __init__(self, settings: Settings) -> None:
        self.resource = create_sql_resource(settings=settings)
        self.engine = self.resource.engine
        self.session_factory = self.resource.session_factory

        OrmEntity.metadata.drop_all(self.engine)
        OrmEntity.metadata.create_all(self.engine)

    def close(self) -> None:
        self.resource.close()


class MongoContext(DatabaseContext):
    def __init__(self, resource: MongoResourceContext) -> None:
        self.database = resource.database

        self._item_factory: ItemMongoFactory | None = None
        self._container_factory: ContainerMongoFactory | None = None

    def teardown(self) -> None:
        for collection in self.database.list_collection_names():
            self.database[collection].delete_many({})

    @property
    def item_factory(self) -> ItemMongoFactory:
        if self._item_factory is None:
            self._item_factory = ItemMongoFactory(database=self.database)
        return self._item_factory

    @property
    def container_factory(self) -> ContainerMongoFactory:
        if self._container_factory is None:
            self._container_factory = ContainerMongoFactory(database=self.database)
        return self._container_factory


class SQLContext(DatabaseContext):
    def __init__(self, resource: SQLResourceContext) -> None:
        self.session = resource.session_factory()

        self._item_factory: ItemSQLFactory | None = None
        self._container_factory: ContainerSQLFactory | None = None

    def teardown(self) -> None:
        for table in reversed(OrmEntity.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()
        self.session.close()

    @property
    def item_factory(self) -> ItemSQLFactory:
        if self._item_factory is None:
            self._item_factory = ItemSQLFactory(session=self.session)
        return self._item_factory

    @property
    def container_factory(self) -> ContainerSQLFactory:
        if self._container_factory is None:
            self._container_factory = ContainerSQLFactory(session=self.session)
        return self._container_factory


@pytest.fixture(scope="session")
def db_resource(settings: Settings) -> Iterator[ResourceContext]:
    resource: ResourceContext

    match settings.repository_type:
        case RepositoryType.MONGO:
            resource = MongoResourceContext(settings=settings)
        case RepositoryType.SQL:
            resource = SQLResourceContext(settings=settings)

    yield resource

    resource.close()


@pytest.fixture
def db_context(
    settings: Settings,
    db_resource: ResourceContext,
) -> Iterator[DatabaseContext]:
    context: DatabaseContext

    match settings.repository_type:
        case RepositoryType.MONGO:
            assert isinstance(db_resource, MongoResourceContext)
            context = MongoContext(resource=db_resource)
        case RepositoryType.SQL:
            assert isinstance(db_resource, SQLResourceContext)
            context = SQLContext(resource=db_resource)

    yield context

    context.teardown()
