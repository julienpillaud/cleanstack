from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.database import Database

from app.core.settings import Settings
from cleanstack.infrastructure.mongo import MongoDocument
from cleanstack.infrastructure.mongo.logger import logger


class MongoResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: MongoClient[MongoDocument]
    database: Database[MongoDocument]

    def release(self) -> None:
        logger.info("MongoDB client released")
        self.client.close()

    def reset(self) -> None:
        for collection in self.database.list_collection_names():
            self.database[collection].delete_many({})


def create_mongo_resource(settings: Settings) -> MongoResource:
    client: MongoClient[MongoDocument] = MongoClient(
        host=str(settings.mongo_uri),
        uuidRepresentation="standard",
    )
    client.admin.command("ping")
    logger.info("MongoDB client up")
    return MongoResource(
        client=client,
        database=client[settings.mongo_database],
    )


@contextmanager
def managed_mongo_session(
    client: MongoClient[MongoDocument],
) -> Iterator[ClientSession]:
    with client.start_session() as session:
        with session.start_transaction():
            yield session
