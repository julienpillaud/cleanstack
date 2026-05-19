from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import Settings
from cleanstack.infrastructure.sql.logger import logger


class SQLResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    def close(self) -> None:
        logger.info("SQL engine close")
        self.engine.dispose()


def create_sql_resource(settings: Settings) -> SQLResource:
    engine = create_engine(
        url=str(settings.postgres_dsn),
        **settings.postgres_params,
    )
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("SQL engine up")
    return SQLResource(
        engine=engine,
        session_factory=sessionmaker(bind=engine),
    )


@contextmanager
def managed_sql_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
