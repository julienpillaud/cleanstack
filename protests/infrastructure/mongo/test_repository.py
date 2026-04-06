from typing import Annotated

from protest import FixtureFactory, ProTestSuite, Use
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.domain.items.entities import Item
from app.infrastructure.mongo.items import AsyncItemMongoRepository
from cleanstack.infrastructure.mongo.types import MongoDocument
from protests.factories.items import get_item
from protests.infrastructure.mongo.fixtures import (
    get_item_repository,
    get_mongo_database,
    get_mongo_session,
)

mongo_repo_suite = ProTestSuite("Mongo repository", tags=["repository"])


@mongo_repo_suite.test()
async def test_create_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    database: Annotated[AsyncDatabase[MongoDocument], Use(get_mongo_database)],
    session: Annotated[AsyncClientSession, Use(get_mongo_session)],
    repository: Annotated[AsyncItemMongoRepository, Use(get_item_repository)],
) -> None:
    new_item = await item_factory()

    await repository.create(new_item)
    await session.commit_transaction()

    result = await database["items"].find_one({"_id": new_item.id})
    assert result
    assert result["_id"] == new_item.id
    assert result["uuid_field"] == new_item.uuid_field
    assert result["string_field"] == new_item.string_field
    assert result["int_field"] == new_item.int_field
    assert result["float_field"] == new_item.float_field
    assert result["bool_field"] == new_item.bool_field
    # assert result["datetime_field"] == new_item.datetime_field
    assert result["strenum_field"] == new_item.strenum_field.value
    assert result["optional_field"] == new_item.optional_field
    # assert result["tags"] == [tag.name for tag in new_item.tags]
    assert result["computed_field"] == new_item.computed_field


@mongo_repo_suite.test()
async def test_update_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    repository: Annotated[AsyncItemMongoRepository, Use(get_item_repository)],
) -> None:
    new_item = await item_factory()
    await repository.create(new_item)

    new_item.string_field = "new_string_field"
    await repository.update(new_item)

    result = await repository.get_by_id(new_item.id)
    assert result
    assert result.string_field == "new_string_field"


@mongo_repo_suite.test()
async def test_get_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    repository: Annotated[AsyncItemMongoRepository, Use(get_item_repository)],
) -> None:
    new_item = await item_factory()
    await repository.create(new_item)

    result = await repository.get_by_id(new_item.id)

    assert result
    assert result.id == new_item.id


@mongo_repo_suite.test()
async def test_get_items(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    repository: Annotated[AsyncItemMongoRepository, Use(get_item_repository)],
) -> None:
    items_count = 3
    for _ in range(items_count):
        new_item = await item_factory()
        await repository.create(new_item)

    results = await repository.get_all()

    assert len(results.items) == items_count
    assert results.total == items_count


@mongo_repo_suite.test()
async def test_delete_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    database: Annotated[AsyncDatabase[MongoDocument], Use(get_mongo_database)],
    repository: Annotated[AsyncItemMongoRepository, Use(get_item_repository)],
) -> None:
    new_item = await item_factory()
    await repository.create(new_item)

    await repository.delete(new_item)

    result = await database["items"].find_one({"_id": new_item.id})
    assert not result
