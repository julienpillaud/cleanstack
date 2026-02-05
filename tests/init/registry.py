from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import Mock

from cleanstack.uow import UnitOfWorkProtocol


class Settings(Mock):
    pass


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self.session = settings.session

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        print("SQL commit")

    def rollback(self) -> None:
        print("SQL rollback")


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self.client = settings.client

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        print("Mongo commit")

    def rollback(self) -> None:
        print("Mongo rollback")
