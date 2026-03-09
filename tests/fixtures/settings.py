import pytest
from pydantic import SecretStr

from app.core.config import Settings


def get_settings_override() -> Settings:
    return Settings(
        environment="test",
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_database="test",
        mongo_database="test",
    )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()
