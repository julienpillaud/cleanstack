from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Protocol

from cleanstack.entities.base import BaseEntity


class AsyncRepositoryProtocol[T: BaseEntity](Protocol):
    async def save(self, entity: T, /) -> None: ...


class BaseFactory[T: BaseEntity](ABC):
    async def create_one(self, **kwargs: Any) -> T:  # noqa: ANN401
        entity = self.build(**kwargs)

        async with self._persistence_context():
            await self._repository.save(entity)

        return entity

    async def create_many(self, count: int, /, **kwargs: Any) -> list[T]:  # noqa: ANN401
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []

        async with self._persistence_context():
            for entity in entities:
                await self._repository.save(entity)
                created_entities.append(entity)

        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...  # noqa: ANN401

    @asynccontextmanager
    @abstractmethod
    def _persistence_context(self) -> AsyncIterator[None]: ...

    @property
    @abstractmethod
    def _repository(self) -> AsyncRepositoryProtocol[T]: ...
