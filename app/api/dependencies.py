from collections.abc import AsyncIterator, Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from app.core.context.mongo import MongoContext, MongoContextProvider
from app.core.context.sql import SQLContext, SQLContextProvider
from app.core.domain import Domain, DomainContext, TransactionProtocol
from app.core.settings import RepositoryType, Settings
from app.domain.context import ContextProtocol
from app.infrastructure.mongo.utils import MongoTransaction
from app.infrastructure.sql.utils import SQLTransaction

type Context = MongoContext | SQLContext


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_transaction(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> TransactionProtocol:
    match settings.repository_type:
        case RepositoryType.SQL:
            sql_engine = request.app.state.sql_resource
            return SQLTransaction(sql_engine)
        case RepositoryType.MONGO:
            mongo_resource = request.app.state.mongo_resource
            return MongoTransaction(mongo_resource)


def get_context_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Callable[[TransactionProtocol], ContextProtocol]:
    match settings.repository_type:
        case RepositoryType.SQL:
            return SQLContextProvider()
        case RepositoryType.MONGO:
            return MongoContextProvider()


async def get_domain(
    transaction: Annotated[TransactionProtocol, Depends(get_transaction)],
    context_provider: Annotated[
        Callable[[TransactionProtocol], ContextProtocol],
        Depends(get_context_provider),
    ],
) -> AsyncIterator[Domain]:
    async with DomainContext(
        transaction=transaction,
        context_provider=context_provider,
    ) as domain:
        yield domain
