from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from faker import Faker

from cleanstack.entities.base import DomainEntity
from cleanstack.factories.base import _BaseFactory
from cleanstack.infrastructure.sql.uow import SQLContext, SQLUnitOfWork


class BaseSQLFactory[T: DomainEntity](_BaseFactory[T], ABC):
    def __init__(self, faker: Faker, context: SQLContext) -> None:
        self.faker = faker
        self.context = context
        self.uow = SQLUnitOfWork(context=context)

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.uow.transaction():
            yield

    def _commit(self) -> None:
        self.uow.commit()
