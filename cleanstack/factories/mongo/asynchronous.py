from abc import ABC
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from pymongo.asynchronous.database import AsyncDatabase

from cleanstack.entities.base import BaseEntity
from cleanstack.factories.asynchronous import BaseFactory
from cleanstack.mongo import MongoDocument


class BaseMongoFactory[T: BaseEntity](BaseFactory[T], ABC):
    def __init__(self, database: AsyncDatabase[MongoDocument]) -> None:
        self.database = database

    @asynccontextmanager
    async def _persistence_context(self) -> AsyncIterator[None]:
        yield
