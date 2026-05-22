from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from pymongo.database import Database

from cleanstack.entities.base import DomainEntity
from cleanstack.factories.base import BaseFactory
from cleanstack.infrastructure.mongo import MongoDocument


class BaseMongoFactory[T: DomainEntity](BaseFactory[T], ABC):
    def __init__(self, database: Database[MongoDocument]) -> None:
        self.database = database

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        yield
