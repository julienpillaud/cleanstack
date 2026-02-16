from typing import Protocol

from cleanstack.context import BaseContextProtocol
from tests.init.adapters import (
    ItemAdapter,
    ItemAdapterProtocol,
    UserAdapter,
    UserAdapterProtocol,
)
from tests.init.uow import (
    UnitOfWork,
)


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def user_adapter(self) -> UserAdapterProtocol: ...

    @property
    def item_adapter(self) -> ItemAdapterProtocol: ...


class Context(ContextProtocol):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def user_adapter(self) -> UserAdapterProtocol:
        return UserAdapter(session=self.uow.sql.session)

    @property
    def item_adapter(self) -> ItemAdapterProtocol:
        return ItemAdapter(client=self.uow.mongo.client)
