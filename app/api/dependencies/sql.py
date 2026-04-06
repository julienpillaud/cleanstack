from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.api.dependencies.settings import get_settings
from app.core.config import Settings
from cleanstack.infrastructure.sql import SQLConfig, SQLUnitOfWork


@lru_cache
def get_sql_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> SQLConfig:
    return SQLConfig.from_settings(url=str(settings.postgres_dsn))


def get_sql_uow(
    context: Annotated[SQLConfig, Depends(get_sql_context)],
) -> SQLUnitOfWork:
    return SQLUnitOfWork(config=context)
