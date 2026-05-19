from protest import fixture
from pydantic import SecretStr

from app.core.settings import AppEnvironment, Settings


# Session scoped fixtures
@fixture()
def get_settings() -> Settings:
    return Settings(
        environment=AppEnvironment.TESTING,
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_database="test",
        mongo_database="test",
    )
