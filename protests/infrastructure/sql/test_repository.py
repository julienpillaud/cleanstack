from typing import Annotated

from protest import FixtureFactory, ProTestSuite, Use
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.domain.items.entities import Item
from app.infrastructure.sql.items import AsyncItemSQLRepository
from app.infrastructure.sql.tables import OrmItem
from protests.factories.items import get_item
from protests.infrastructure.sql.fixtures import get_engine

sql_repo_suite = ProTestSuite("SQL repository", tags=["repository"])


@sql_repo_suite.test()
async def test_create_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    engine: Annotated[AsyncEngine, Use(get_engine)],
) -> None:
    new_item = await item_factory()

    async with AsyncSession(engine) as session:
        repository = AsyncItemSQLRepository(session=session)
        await repository.save(new_item)
        await session.commit()

    async with AsyncSession(engine) as session:
        result = await session.get(OrmItem, new_item.id)

    assert result
    assert result.id == new_item.id


@sql_repo_suite.test()
async def test_update_item(
    item_factory: Annotated[FixtureFactory[Item], Use(get_item)],
    engine: Annotated[AsyncEngine, Use(get_engine)],
) -> None:
    new_item = await item_factory()

    async with AsyncSession(engine) as session:
        repository = AsyncItemSQLRepository(session=session)
        await repository.save(new_item)
        await session.commit()

    async with AsyncSession(engine) as session:
        repository = AsyncItemSQLRepository(session=session)
        updated_item = new_item
        updated_item.string_field = "new_string_field"
        await repository.update(updated_item)
        await session.commit()

    async with AsyncSession(engine) as session:
        result = await session.get(OrmItem, new_item.id)

    assert result
    assert result.string_field == "new_string_field"
