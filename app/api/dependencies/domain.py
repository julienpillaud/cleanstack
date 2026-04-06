from typing import Annotated

from fastapi import Depends

from app.api.dependencies.mongo import get_mongo_uow
from app.api.dependencies.settings import get_settings
from app.api.dependencies.sql import get_sql_uow
from app.core.config import RepositoryType, Settings
from app.core.context.mongo import MongoContext
from app.core.context.sql import SQLContext
from app.domain.domain import Domain
from cleanstack.domain import CompositeUniOfWork
from cleanstack.infrastructure.mongo import MongoUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
) -> MongoContext | SQLContext:
    match settings.repository_type:
        case RepositoryType.MONGO:
            return MongoContext(mongo_uow=mongo_uow)
        case RepositoryType.SQL:
            return SQLContext(sql_uow=sql_uow)


def get_domain(
    context: Annotated[MongoContext | SQLContext, Depends(get_context)],
) -> Domain:
    uow = CompositeUniOfWork(members=context.members)
    return Domain(uow=uow, context=context)
