import pytest

from tests.factories.entities import DBEntity
from tests.factories.factories import PostFactory, UserFactory


@pytest.fixture
def collection() -> list[DBEntity]:
    return []


@pytest.fixture
def user_factory(collection: list[DBEntity]) -> UserFactory:
    return UserFactory(collection=collection)


@pytest.fixture
def post_factory(collection: list[DBEntity]) -> PostFactory:
    return PostFactory(collection=collection)
