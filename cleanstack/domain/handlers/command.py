import time
from collections.abc import Callable
from typing import Concatenate

from cleanstack.domain.context import BaseContextProtocol
from cleanstack.domain.domain import BaseDomain
from cleanstack.domain.handlers.base import BaseBound, BaseHandler
from cleanstack.domain.uow import UnitOfWorkProtocol


class CommandBound[U: UnitOfWorkProtocol, C: BaseContextProtocol, **P, R](
    BaseBound[U, C, P, R]
):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        uow = self.instance.uow
        with uow.transaction():
            try:
                result = self.func(self.instance.context, *args, **kwargs)
            except Exception:
                uow.rollback()
                raise

            uow.commit()
            self._log_success(start_time)
            return result


class CommandHandler[C: BaseContextProtocol, **P, R](BaseHandler[C, P, R]):
    def _get_bound(
        self,
        func: Callable[Concatenate[C, P], R],
        instance: BaseDomain[UnitOfWorkProtocol, C],
    ) -> Callable[P, R]:
        return CommandBound(func, instance)
