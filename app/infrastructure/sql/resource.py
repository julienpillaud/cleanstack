from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import Settings
from app.infrastructure.sql.logger import logger
from cleanstack.sql.entities import OrmEntity


@dataclass(frozen=True)
class SQLResource:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    @classmethod
    async def from_settings(cls, settings: Settings, /) -> SQLResource:
        engine = create_async_engine(
            url=str(settings.postgres_dsn),
            **settings.postgres_params,
        )
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        logger.info("SQL engine up")
        return cls(
            engine=engine,
            session_factory=async_sessionmaker(bind=engine),
        )

    async def release(self) -> None:
        logger.info("SQL engine released")
        await self.engine.dispose()

    async def init(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(OrmEntity.metadata.drop_all)
            await connection.run_sync(OrmEntity.metadata.create_all)

    async def reset(self) -> None:
        async with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()
