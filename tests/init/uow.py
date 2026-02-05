from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import MagicMock

from cleanstack.uow import UnitOfWorkProtocol


class Settings(MagicMock):
    pass


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self.session = settings.session

    @contextmanager
    def transaction(self) -> Iterator[None]:
        print("SQL before transaction")
        yield
        print("SQL after transaction")

    def commit(self) -> None:
        print("SQL commit")

    def rollback(self) -> None:
        print("SQL rollback")


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self.client = settings.client

    @contextmanager
    def transaction(self) -> Iterator[None]:
        print("Mongo before transaction")
        yield
        print("Mongo after transaction")

    def commit(self) -> None:
        print("Mongo commit")

    def rollback(self) -> None:
        print("Mongo rollback")
