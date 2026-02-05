from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from typing import Protocol


class UnitOfWorkProtocol(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[None]: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class CompositeUniOfWork(UnitOfWorkProtocol):
    members: list[UnitOfWorkProtocol]

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
