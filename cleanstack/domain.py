import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, Generic, ParamSpec, Protocol, TypeVar

from cleanstack.logger import logger

P = ParamSpec("P")
R = TypeVar("R")


class ContextProtocol(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[None]: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class CommandHandler(Generic[P, R]):
    def __init__(self, func: Callable[Concatenate[ContextProtocol, P], R]) -> None:
        self.func = func

    def __get__(
        self, instance: "BaseDomain", owner: type["BaseDomain"]
    ) -> Callable[P, R]:
        logger.debug(f"Command '{self.func.__name__}' bound")
        return instance.command_handler(self.func)


class BaseDomain:
    def __init__(self, context: ContextProtocol):
        logger.debug("Instantiate 'Domain'")
        self.context = context

    def command_handler(
        self, func: Callable[Concatenate[ContextProtocol, P], R]
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                # Catch all exceptions to ensure rollback
                except Exception as error:
                    self.context.rollback()
                    logger.info(
                        f"Command '{func.__name__}' failed with "
                        f"{error.__class__.__name__}: {error}"
                    )
                    raise

                self.context.commit()
                duration = time.perf_counter() - start_time
                logger.info(
                    f"Command '{func.__name__}' succeeded in {duration * 1000:.1f} ms",
                )
                return result

        return wrapper
