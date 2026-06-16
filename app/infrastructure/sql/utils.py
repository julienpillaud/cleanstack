from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import Settings
from app.infrastructure.sql.logger import logger
from cleanstack.sql.entities import OrmEntity


class SQLResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    @classmethod
    def from_settings(cls, settings: Settings, /) -> SQLResource:
        engine = create_engine(
            url=str(settings.postgres_dsn),
            **settings.postgres_params,
        )
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("SQL engine up")
        return cls(
            engine=engine,
            session_factory=sessionmaker(bind=engine),
        )

    def create_all(self) -> None:
        OrmEntity.metadata.drop_all(self.engine)
        OrmEntity.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        _session = self.session_factory()
        try:
            yield _session
            _session.commit()
            logger.info("Commit ok")
        except Exception as error:
            logger.error(f"Rollback due to {error}")
            _session.rollback()
            raise
        finally:
            _session.close()

    def release(self) -> None:
        logger.info("SQL engine released")
        self.engine.dispose()

    def reset(self) -> None:
        with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()
