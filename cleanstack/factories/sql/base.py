from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from cleanstack.entities.base import DomainEntity
from cleanstack.factories.base import _BaseFactory


class BaseSQLFactory[T: DomainEntity](_BaseFactory[T], ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        yield
        self.session.commit()
