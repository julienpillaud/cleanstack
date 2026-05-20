from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from cleanstack.domain.repository import SyncRepositoryProtocol
from cleanstack.entities.base import DomainEntity


class _BaseFactory[T: DomainEntity](ABC):
    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)

        with self._persistence_context():
            self._repository.save(entity)

        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []

        with self._persistence_context():
            for entity in entities:
                self._repository.save(entity)
                created_entities.append(entity)

        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...

    @contextmanager
    @abstractmethod
    def _persistence_context(self) -> Iterator[None]: ...

    @property
    @abstractmethod
    def _repository(self) -> SyncRepositoryProtocol[T]: ...
