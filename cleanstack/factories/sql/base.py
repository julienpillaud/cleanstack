from abc import ABC
from collections.abc import Callable, Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from cleanstack.entities.base import BaseEntity
from cleanstack.factories.base import BaseFactory


class BaseSQLFactory[T: BaseEntity](BaseFactory[T], ABC):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory
        self._session: Session | None = None

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.session_factory() as session:
            self._session = session
            yield
            session.commit()
        self._session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError()
        return self._session
