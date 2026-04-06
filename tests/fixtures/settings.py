from collections.abc import Callable
from functools import lru_cache

import pytest
from pydantic import SecretStr

from app.core.config import AppEnvironment, RepositoryType, Settings


@lru_cache
def get_mongo_settings() -> Settings:
    return Settings(
        environment=AppEnvironment.TESTING,
        repository_type=RepositoryType.MONGO,
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_database="test",
        mongo_database="test",
    )


@lru_cache
def get_sql_settings() -> Settings:
    return Settings(
        environment=AppEnvironment.TESTING,
        repository_type=RepositoryType.SQL,
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_database="test",
        mongo_database="test",
    )


@pytest.fixture(
    scope="session",
    params=[RepositoryType.MONGO, RepositoryType.SQL],
)
def settings_override_func(request: pytest.FixtureRequest) -> Callable[[], Settings]:
    match request.param:
        case RepositoryType.MONGO:
            return get_mongo_settings
        case RepositoryType.SQL:
            return get_sql_settings
        case _:
            raise RuntimeError()


@pytest.fixture(scope="session")
def settings(settings_override_func: Callable[[], Settings]) -> Settings:
    return settings_override_func()
