from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from app.core.config import RepositoryType, Settings
from cleanstack.infrastructure.mongo import MongoConfig
from cleanstack.infrastructure.sql import SQLConfig
from cleanstack.infrastructure.sql.entities import OrmEntity


@pytest.fixture(scope="session")
def repo_config(settings: Settings) -> MongoConfig | SQLConfig:
    match settings.repository_type:
        case RepositoryType.MONGO:
            return MongoConfig.from_settings(
                host=str(settings.mongo_dsn),
                database_name=settings.mongo_database,
            )
        case RepositoryType.SQL:
            return SQLConfig.from_settings(url=str(settings.postgres_dsn))


@pytest.fixture(autouse=True)
def clean_repo(repo_config: MongoConfig | SQLConfig) -> Iterator[None]:
    yield

    if isinstance(repo_config, MongoConfig):
        database = repo_config.database
        for collection in database.list_collection_names():
            database[collection].delete_many({})

    if isinstance(repo_config, SQLConfig):
        with Session(repo_config.engine) as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()
