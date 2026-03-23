from app.core.config import Settings
from cleanstack.infrastructure.sql.entities import OrmEntity
from cleanstack.infrastructure.sql.uow import SQLContext


def initialize_app(settings: Settings) -> None:
    initialize_sql_database(settings=settings)


def initialize_sql_database(settings: Settings) -> None:
    """Only used in this project for convenience."""
    context = SQLContext.from_settings(url=str(settings.postgres_dsn))
    OrmEntity.metadata.create_all(context.engine)
