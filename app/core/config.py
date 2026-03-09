from pydantic import MongoDsn, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    project_name: str = "clean-app"
    api_version: str = "1.0.0"
    environment: str

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str

    mongo_user: str | None = None
    mongo_password: SecretStr | None = None
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_rs_name: str = "rs0"
    mongo_database: str

    @computed_field  # type: ignore
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_database,
        )

    @computed_field  # type: ignore
    @property
    def mongo_dsn(self) -> MongoDsn:
        query = f"replicaSet={self.mongo_rs_name}" if self.mongo_rs_name else None
        return MongoDsn.build(
            scheme="mongodb",
            host="localhost",
            username=self.mongo_user,
            password=self.mongo_password.get_secret_value()
            if self.mongo_password
            else None,
            port=self.mongo_port,
            query=query,
        )
