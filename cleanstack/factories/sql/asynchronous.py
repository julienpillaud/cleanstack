from abc import ABC
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from cleanstack.entities.base import BaseEntity
from cleanstack.factories.asynchronous import BaseFactory


class BaseSQLFactory[T: BaseEntity](BaseFactory[T], ABC):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self.session_factory = session_factory
        self._session: AsyncSession | None = None

    @asynccontextmanager
    async def _persistence_context(self) -> AsyncIterator[None]:
        async with self.session_factory() as session:
            self._session = session
            yield
            await session.commit()
        self._session = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError()
        return self._session
