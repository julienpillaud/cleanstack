from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from typing import Protocol


class UnitOfWorkProtocol(Protocol):
    @contextmanager
    def scope(self) -> Iterator[None]:
        """Provides a lightweight execution context for read-only operations."""

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Provides an atomic execution context for write operations."""

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class CompositeUniOfWork(UnitOfWorkProtocol):
    def __init__(self, members: list[UnitOfWorkProtocol]) -> None:
        self.members = members

    @contextmanager
    def scope(self) -> Iterator[None]:
        with ExitStack() as stack:
            for member in self.members:
                stack.enter_context(member.scope())
            yield

    @contextmanager
    def transaction(self) -> Iterator[None]:
        with ExitStack() as stack:
            for member in self.members:
                stack.enter_context(member.transaction())
            yield

    def commit(self) -> None:
        for member in self.members:
            member.commit()

    def rollback(self) -> None:
        for member in reversed(self.members):
            member.rollback()
