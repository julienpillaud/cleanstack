from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.api.dependencies.settings import get_settings
from app.core.config import Settings
from cleanstack.infrastructure.mongo import MongoConfig, MongoUnitOfWork


@lru_cache
def get_mongo_config(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoConfig:
    return MongoConfig.from_settings(
        host=str(settings.mongo_dsn),
        database_name=settings.mongo_database,
    )


def get_mongo_uow(
    context: Annotated[MongoConfig, Depends(get_mongo_config)],
) -> MongoUnitOfWork:
    return MongoUnitOfWork(config=context)
