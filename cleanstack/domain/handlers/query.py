from collections.abc import Callable
from typing import Concatenate

from cleanstack.domain.context import BaseContextProtocol
from cleanstack.domain.domain import BaseDomain
from cleanstack.domain.handlers.base import BaseBound, BaseHandler
from cleanstack.domain.uow import UnitOfWorkProtocol


class QueryBound[U: UnitOfWorkProtocol, C: BaseContextProtocol, **P, R](
    BaseBound[U, C, P, R]
):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        uow = self.instance.uow
        with uow.scope():
            try:
                result = self.func(self.instance.context, *args, **kwargs)
            except Exception as error:
                self._log_error(error)
                raise
            return result


class QueryHandler[C: BaseContextProtocol, **P, R](BaseHandler[C, P, R]):
    def _get_bound(
        self,
        func: Callable[Concatenate[C, P], R],
        instance: BaseDomain[UnitOfWorkProtocol, C],
    ) -> Callable[P, R]:
        return QueryBound(func, instance)
