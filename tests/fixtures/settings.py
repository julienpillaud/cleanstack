import pytest

from app.core.config import Settings


def get_settings_override() -> Settings:
    return Settings(mongo_database="test")


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()
