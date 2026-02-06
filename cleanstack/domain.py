import time
from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from cleanstack.logger import logger
from cleanstack.uow import UnitOfWorkProtocol


class BaseHandler[T: UnitOfWorkProtocol, **P, R]:
    """Base descriptor for binding a command to a Domain instance.

    It applies a decorator to wrap the command in a unit-of-work transaction.
    The binding occurs lazily when the command is accessed but then cached in the
    instance's `__dict__` for the following accesses.

    It allows declaring commands in a simple way as class attribute:

    ```python
    class Domain(BaseDomain[ContextProtocol]):
        get_users = QueryHandler(get_users_command)
        create_user = CommandHandler(create_user_command)
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

        bound = self._get_bound_func(instance)
        logger.debug(f"Bound command '{self.name}'")

        instance.__dict__[self.name] = bound
        return bound

    def _get_bound_func(self, instance: BaseDomain[T]) -> Callable[P, R]:
        raise NotImplementedError


class QueryHandler[T: UnitOfWorkProtocol, **P, R](BaseHandler[T, P, R]):
    """Descriptor for read-only operations without commit."""

    def _get_bound_func(self, instance: BaseDomain[T]) -> Callable[P, R]:
        return instance.query_handler(self.func)


class CommandHandler[T: UnitOfWorkProtocol, **P, R](BaseHandler[T, P, R]):
    """Descriptor for write operations with commit/rollback logic."""

    def _get_bound_func(self, instance: BaseDomain[T]) -> Callable[P, R]:
        return instance.command_handler(self.func)


class BaseDomain[T: UnitOfWorkProtocol]:
    def __init__(self, context: T):
        self.context = context

    def query_handler[**P, R](
        self,
        func: Callable[Concatenate[T, P], R],
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                except Exception as error:
                    self._log_error(func, error)
                    raise

            self._log_success(start_time, func)
            return result

        return wrapper

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
                    self._log_error(func, error)
                    raise

                self.context.commit()
                self._log_success(start_time, func)
                return result

        return wrapper

    @staticmethod
    def _log_error[**P, R](
        func: Callable[Concatenate[T, P], R],
        error: Exception,
    ) -> None:
        func_name = getattr(func, "__name__", "unknown_command")
        logger.info(
            f"Command '{func_name}' failed with {error.__class__.__name__}: {error}"
        )

    @staticmethod
    def _log_success[**P, R](
        start_time: float,
        func: Callable[Concatenate[T, P], R],
    ) -> None:
        duration = (time.perf_counter() - start_time) * 1000
        func_name = getattr(func, "__name__", "unknown_command")
        logger.info(
            f"Command '{func_name}' succeeded in {duration:.1f} ms",
        )
