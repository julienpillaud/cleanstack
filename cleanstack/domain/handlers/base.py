import time
from collections.abc import Callable
from typing import Concatenate, Self, overload

from cleanstack.domain.context import BaseContextProtocol
from cleanstack.domain.domain import BaseDomain
from cleanstack.domain.logger import logger
from cleanstack.domain.uow import UnitOfWorkProtocol


class BaseHandler[C: BaseContextProtocol, **P, R]:
    def __init__(self, func: Callable[Concatenate[C, P], R]) -> None:
        self.func = func

    def __set_name__(
        self,
        owner: type[BaseDomain[UnitOfWorkProtocol, C]],
        name: str,
    ) -> None:
        self.name = name

    @overload
    def __get__(
        self,
        instance: None,
        owner: type[BaseDomain[UnitOfWorkProtocol, C]],
    ) -> Self: ...

    @overload
    def __get__(
        self,
        instance: BaseDomain[UnitOfWorkProtocol, C],
        owner: type[BaseDomain[UnitOfWorkProtocol, C]],
    ) -> Callable[P, R]: ...

    def __get__(
        self,
        instance: BaseDomain[UnitOfWorkProtocol, C] | None,
        owner: type[BaseDomain[UnitOfWorkProtocol, C]],
    ) -> Self | Callable[P, R]:
        if instance is None:
            return self

        if self.name in instance.__dict__:
            return instance.__dict__[self.name]  # type: ignore

        bound = self._get_bound(self.func, instance)
        instance.__dict__[self.name] = bound
        return bound

    def _get_bound(
        self,
        func: Callable[Concatenate[C, P], R],
        instance: BaseDomain[UnitOfWorkProtocol, C],
    ) -> Callable[P, R]:
        raise NotImplementedError


class BaseBound[U: UnitOfWorkProtocol, C: BaseContextProtocol, **P, R]:
    def __init__(
        self,
        func: Callable[Concatenate[C, P], R],
        instance: BaseDomain[U, C],
    ) -> None:
        self.func = func
        self.func_name = getattr(self.func, "__name__", "unknown_command")
        self.instance = instance

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        raise NotImplementedError

    def _log_error(self, error: Exception) -> None:
        error_name = error.__class__.__name__
        logger.info(f"Command '{self.func_name}' failed with {error_name}: {error}")

    def _log_success(self, start_time: float) -> None:
        duration = (time.perf_counter() - start_time) * 1000
        logger.info(f"Command '{self.func_name}' succeeded in {duration:.1f} ms")
