from collections.abc import AsyncIterator
from typing import Annotated

from apte import Use, fixture
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase

from app.core.settings import Settings
from app.infrastructure.mongo.items import ItemMongoRepository
from cleanstack.mongo import MongoDocument
from tests_apte.fixtures import get_settings


@fixture()
async def get_mongo_client(
    settings: Annotated[Settings, Use(get_settings)],
) -> AsyncIterator[AsyncMongoClient[MongoDocument]]:
    async with AsyncMongoClient[MongoDocument](
        host=str(settings.mongo_uri),
        uuidRepresentation="standard",
    ) as client:
        yield client


@fixture()
async def get_mongo_database(
    settings: Annotated[Settings, Use(get_settings)],
    client: Annotated[AsyncMongoClient[MongoDocument], Use(get_mongo_client)],
) -> AsyncIterator[AsyncDatabase[MongoDocument]]:
    database = client[settings.mongo_database]

    yield database

    for collection in await database.list_collection_names():
        await database[collection].delete_many({})


@fixture()
async def get_mongo_session(
    client: Annotated[AsyncMongoClient[MongoDocument], Use(get_mongo_client)],
) -> AsyncIterator[AsyncClientSession]:
    async with client.start_session() as session, await session.start_transaction():
        yield session


@fixture()
async def get_item_repository(
    database: Annotated[AsyncDatabase[MongoDocument], Use(get_mongo_database)],
    session: Annotated[AsyncClientSession, Use(get_mongo_session)],
) -> ItemMongoRepository:
    return ItemMongoRepository(database=database, session=session)
