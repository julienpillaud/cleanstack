import time
from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from cleanstack.logger import logger
from cleanstack.uow import UnitOfWorkProtocol


class CommandHandler[T: UnitOfWorkProtocol, **P, R]:
    """Descriptor for binding a command to a Domain instance.

    It applies a decorator to wrap the command in a unit-of-work transaction.
    The binding occurs lazily when the command is accessed but then cached in the
    instance's `__dict__` for the following accesses.

    It allows declaring commands in a simple way as class attribute:

    ```python
    class Domain(BaseDomain[ContextProtocol]):
        get_users = CommandHandler(get_users_command)
    ```
    """

    def __init__(self, func: Callable[Concatenate[T, P], R]) -> None:
        self.func = func

    def __set_name__(self, owner: type[BaseDomain[T]], name: str) -> None:
        self.name = name

    def __get__(
        self,
        instance: BaseDomain[T],
        owner: type[BaseDomain[T]],
    ) -> Callable[P, R]:
        if instance is None:
            return self

        if self.name in instance.__dict__:
            return instance.__dict__[self.name]  # type: ignore

        bound = instance.command_handler(self.func)
        logger.debug(f"Bound command '{self.name}'")

        instance.__dict__[self.name] = bound
        return bound


class BaseDomain[T: UnitOfWorkProtocol]:
    def __init__(self, context: T):
        self.context = context

    def command_handler[**P, R](
        self,
        func: Callable[Concatenate[T, P], R],
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
