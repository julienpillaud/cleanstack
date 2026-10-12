from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.protocols import UnitOfWorkProtocol
from app.infrastructure.sql.logger import logger
from app.infrastructure.sql.resource import SQLResource


class SQLUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, resource: SQLResource, /) -> None:
        self.resource = resource
        self.session: AsyncSession | None = None

    async def start(self, transactional: bool) -> None:
        self.session = self.resource.session_factory()

    async def end(self, error: BaseException | None) -> None:
        if not self.session:
            return

        try:
            if error is None:
                await self.session.commit()
                logger.debug("Transaction committed")
            else:
                await self.session.rollback()
                logger.warning("Transaction rollback")
        finally:
            await self.session.close()
