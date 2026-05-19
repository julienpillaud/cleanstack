import pytest

from tests.plugins.database import ContainerFactory, DatabaseContext, ItemFactory


@pytest.fixture
def item_factory(db_context: DatabaseContext) -> ItemFactory:
    return db_context.item_factory


@pytest.fixture
def container_factory(db_context: DatabaseContext) -> ContainerFactory:
    return db_context.container_factory
