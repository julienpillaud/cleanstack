from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from pymongo.database import Database

from cleanstack.entities.base import BaseEntity
from cleanstack.factories.base import BaseFactory
from cleanstack.mongo import MongoDocument


class BaseMongoFactory[T: BaseEntity](BaseFactory[T], ABC):
    def __init__(self, database: Database[MongoDocument]) -> None:
        self.database = database

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        yield
