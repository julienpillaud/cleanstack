from collections.abc import AsyncIterator
from typing import Annotated

from protest import Use, fixture
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import Settings
from app.infrastructure.mongo.items import AsyncItemMongoRepository
from cleanstack.infrastructure.mongo.types import MongoDocument
from protests.fixtures import settings


@fixture()
async def mongo_database(
    settings: Annotated[Settings, Use(settings)],
) -> AsyncIterator[AsyncDatabase[MongoDocument]]:
    async with AsyncMongoClient[MongoDocument](
        host=str(settings.mongo_dsn),
        uuidRepresentation="standard",
    ) as client:
        database = client[settings.mongo_database]

        yield database

        for collection in await database.list_collection_names():
            await database[collection].delete_many({})


@fixture()
async def item_repository(
    database: Annotated[AsyncDatabase[MongoDocument], Use(mongo_database)],
) -> AsyncItemMongoRepository:
    return AsyncItemMongoRepository(database=database)
