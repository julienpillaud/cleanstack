from dataclasses import dataclass

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.settings import Settings
from app.infrastructure.mongo.logger import logger
from cleanstack.mongo import MongoDocument


@dataclass(frozen=True)
class MongoResource:
    client: AsyncMongoClient[MongoDocument]
    database: AsyncDatabase[MongoDocument]

    @classmethod
    async def from_settings(cls, settings: Settings, /) -> MongoResource:
        client: AsyncMongoClient[MongoDocument] = AsyncMongoClient(
            host=str(settings.mongo_uri),
            uuidRepresentation="standard",
        )
        await client.admin.command("ping")
        logger.info("MongoDB client up")
        return cls(
            client=client,
            database=client[settings.mongo_database],
        )

    async def release(self) -> None:
        logger.info("MongoDB client released")
        await self.client.close()

    async def reset(self) -> None:
        for collection in await self.database.list_collection_names():
            await self.database[collection].delete_many({})
