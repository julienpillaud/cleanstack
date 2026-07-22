from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import TransactionProtocol
from app.domain.containers.repository import ContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sql.containers import ContainerSQLRepository
from app.infrastructure.sql.items import ItemSQLRepository
from app.infrastructure.sql.utils import SQLTransaction


class SQLContext(ContextProtocol):
    def __init__(self, transaction: SQLTransaction) -> None:
        self.transaction = transaction

    @property
    def session(self) -> AsyncSession:
        if self.transaction.session is None:
            raise RuntimeError()
        return self.transaction.session

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.session)

    @cached_property
    def container_repository(self) -> ContainerRepositoryProtocol:
        return ContainerSQLRepository(session=self.session)


class SQLContextProvider:
    def __call__(self, transaction: TransactionProtocol) -> SQLContext:
        if not isinstance(transaction, SQLTransaction):
            raise RuntimeError()

        return SQLContext(transaction=transaction)
