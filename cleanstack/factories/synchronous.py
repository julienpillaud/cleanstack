from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Protocol

from cleanstack.entities.base import BaseEntity


class SyncRepositoryProtocol[T: BaseEntity](Protocol):
    def save(self, entity: T, /) -> None: ...


class BaseFactory[T: BaseEntity](ABC):
    def create_one(self, **kwargs: Any) -> T:  # noqa: ANN401
        entity = self.build(**kwargs)

        with self._persistence_context():
            self._repository.save(entity)

        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:  # noqa: ANN401
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []

        with self._persistence_context():
            for entity in entities:
                self._repository.save(entity)
                created_entities.append(entity)

        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...  # noqa: ANN401

    @contextmanager
    @abstractmethod
    def _persistence_context(self) -> Iterator[None]: ...

    @property
    @abstractmethod
    def _repository(self) -> SyncRepositoryProtocol[T]: ...
