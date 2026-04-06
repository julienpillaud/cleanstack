from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.entities.base import DomainEntity
from cleanstack.factories.base import _BaseFactory
from cleanstack.infrastructure.mongo.uow import MongoConfig, MongoUnitOfWork


class BaseMongoFactory[T: DomainEntity](_BaseFactory[T], ABC):
    def __init__(self, config: MongoConfig) -> None:
        self.config = config
        self.uow = MongoUnitOfWork(config=config)

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.uow.transaction():
            yield

    def _commit(self) -> None:
        self.uow.commit()
