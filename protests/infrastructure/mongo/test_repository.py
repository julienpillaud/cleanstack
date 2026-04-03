from typing import Annotated

from protest import FixtureFactory, ProTestSuite, Use

from app.domain.items.entities import Item
from cleanstack.infrastructure.mongo.asynchronous.repository import AsyncMongoRepository
from protests.factories.items import item
from protests.infrastructure.mongo.fixtures import item_repository

mongo_repo_suite = ProTestSuite("MongoRepo", tags=["repository"])


@mongo_repo_suite.test()
async def test_repo(
    item_factory: Annotated[FixtureFactory[Item], Use(item)],
    repository: Annotated[AsyncMongoRepository[Item], Use(item_repository)],
) -> None:
    new_item = await item_factory()

    await repository.create(new_item)

    result = await repository.get_by_id(new_item.id)

    assert result
