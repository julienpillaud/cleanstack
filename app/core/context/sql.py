from app.domain.context import ContextProtocol
from app.domain.items.repository import SyncItemRepositoryProtocol
from app.infrastructure.sql.items import SyncItemSQLRepository
from cleanstack.domain import UnitOfWorkProtocol
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork


class SQLContext(ContextProtocol):
    def __init__(self, sql_uow: SQLUnitOfWork):
        self.sql_uow = sql_uow
        self.members: list[UnitOfWorkProtocol] = [self.sql_uow]

    @property
    def item_repository(self) -> SyncItemRepositoryProtocol:
        return SyncItemSQLRepository(session=self.sql_uow.session)
