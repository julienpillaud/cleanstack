from functools import cached_property

from sqlalchemy.orm import Session

from app.domain.containers.repository import SyncContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import SyncItemRepositoryProtocol
from app.infrastructure.sql.containers import SyncContainerSQLRepository
from app.infrastructure.sql.items import SyncItemSQLRepository


class SQLContext(ContextProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    @cached_property
    def item_repository(self) -> SyncItemRepositoryProtocol:
        return SyncItemSQLRepository(session=self.session)

    @cached_property
    def container_repository(self) -> SyncContainerRepositoryProtocol:
        return SyncContainerSQLRepository(session=self.session)
