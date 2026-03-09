from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from app.core.config import Settings
from cleanstack.infrastructure.sql.entities import OrmEntity
from cleanstack.infrastructure.sql.uow import SQLContext


@pytest.fixture(scope="session")
def sql_context(settings: Settings) -> SQLContext:
    context = SQLContext.from_settings(url=str(settings.postgres_dsn))
    engine = context.engine

    OrmEntity.metadata.drop_all(engine)
    OrmEntity.metadata.create_all(engine)

    return context


@pytest.fixture(autouse=True)
def clean_sql(sql_context: SQLContext) -> Iterator[None]:
    yield
    with Session(sql_context.engine) as session:
        for table in reversed(OrmEntity.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
