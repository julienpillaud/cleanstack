from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.protocols import UnitOfWorkProtocol
from app.domain.containers.repository import ContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.containers import ContainerSQLRepository
from app.infrastructure.sql.items import ItemSQLRepository
from app.infrastructure.sql.uow import SQLUnitOfWork


class SQLContext(ContextProtocol):
    def __init__(self, uow: SQLUnitOfWork) -> None:
        self.uow = uow

    @property
    def session(self) -> AsyncSession:
        if self.uow.session is None:
            raise RuntimeError()

        return self.uow.session

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.session)

    @cached_property
    def container_repository(self) -> ContainerRepositoryProtocol:
        return ContainerSQLRepository(session=self.session)


class SQLContextProvider:
    def __call__(self, uow: UnitOfWorkProtocol) -> SQLContext:
        if not isinstance(uow, SQLUnitOfWork):
            raise RuntimeError()

        return SQLContext(uow=uow)
