from cleanstack.domain.context import BaseContextProtocol
from cleanstack.domain.uow import UnitOfWorkProtocol


class BaseDomain[U: UnitOfWorkProtocol, C: BaseContextProtocol]:
    def __init__(self, uow: U, context: C) -> None:
        self.uow = uow
        self.context = context
