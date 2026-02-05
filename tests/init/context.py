from typing import Protocol

from cleanstack.uow import CompositeUniOfWork, UnitOfWorkProtocol
from tests.init.adapters import (
    ItemAdapter,
    ItemAdapterProtocol,
    UserAdapter,
    UserAdapterProtocol,
)
from tests.init.uow import (
    MongoUnitOfWork,
    Settings,
    SQLUnitOfWork,
)


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def user_adapter(self) -> UserAdapterProtocol: ...

    @property
    def item_adapter(self) -> ItemAdapterProtocol: ...


class Context(CompositeUniOfWork, ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        self.sql_uow = SQLUnitOfWork(settings=settings)
        self.mongo_uow = MongoUnitOfWork(settings=settings)
        self.members = [self.sql_uow, self.mongo_uow]

    @property
    def user_adapter(self) -> UserAdapterProtocol:
        return UserAdapter(session=self.sql_uow.session)

    @property
    def item_adapter(self) -> ItemAdapterProtocol:
        return ItemAdapter(client=self.mongo_uow.client)
