from collections.abc import AsyncIterator
from typing import Annotated

from protest import Use, fixture
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import Settings
from app.infrastructure.sql.items import AsyncItemSQLRepository
from cleanstack.sql.entities import OrmEntity
from protests.fixtures import get_settings


@fixture()
async def get_engine(
    settings: Annotated[Settings, Use(get_settings)],
) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(url=str(settings.postgres_dsn))

    async with engine.begin() as conn:
        await conn.run_sync(OrmEntity.metadata.drop_all)
        await conn.run_sync(OrmEntity.metadata.create_all)

    yield engine

    await engine.dispose()


@fixture()
async def get_session_factory(
    engine: Annotated[AsyncEngine, Use(get_engine)],
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine)


@fixture()
async def get_sql_session(
    async_session: Annotated[
        async_sessionmaker[AsyncSession], Use(get_session_factory)
    ],
) -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


@fixture()
async def get_sql_item_repository(
    session: Annotated[AsyncSession, Use(get_sql_session)],
) -> AsyncItemSQLRepository:
    return AsyncItemSQLRepository(session=session)
