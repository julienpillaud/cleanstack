from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from app.core.context.mongo import MongoContext, MongoContextProvider
from app.core.context.sql import SQLContext, SQLContextProvider
from app.core.domain import Domain, DomainScope
from app.core.protocols import ContextProviderProtocol, UnitOfWorkProtocol
from app.core.settings import RepositoryType, Settings
from app.infrastructure.mongo.uow import MongoUnitOfWork
from app.infrastructure.sql.uow import SQLUnitOfWork

type Context = MongoContext | SQLContext


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_uow(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> UnitOfWorkProtocol:
    match settings.repository_type:
        case RepositoryType.SQL:
            sql_resource = request.app.state.sql_resource
            return SQLUnitOfWork(sql_resource)
        case RepositoryType.MONGO:
            mongo_resource = request.app.state.mongo_resource
            return MongoUnitOfWork(mongo_resource)


def get_context_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ContextProviderProtocol:
    match settings.repository_type:
        case RepositoryType.SQL:
            return SQLContextProvider()
        case RepositoryType.MONGO:
            return MongoContextProvider()


class DomainProvider:
    def __init__(self, *, transactional: bool = False) -> None:
        self.transactional = transactional

    async def __call__(
        self,
        uow: Annotated[UnitOfWorkProtocol, Depends(get_uow)],
        context_provider: Annotated[
            ContextProviderProtocol, Depends(get_context_provider)
        ],
    ) -> AsyncIterator[Domain]:
        async with DomainScope(
            uow=uow,
            context_provider=context_provider,
            transactional=self.transactional,
        ) as domain:
            yield domain


QueryDomain = Annotated[Domain, Depends(DomainProvider(), scope="function")]
CommandDomain = Annotated[
    Domain,
    Depends(DomainProvider(transactional=True), scope="function"),
]
