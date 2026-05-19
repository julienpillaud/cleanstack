from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pymongo import MongoClient
from pymongo.synchronous.client_session import ClientSession
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.context.mongo import MongoContext
from app.core.context.sql import SQLContext
from app.core.settings import RepositoryType, Settings
from app.infrastructure.mongo.utils import managed_mongo_session
from app.infrastructure.sql.utils import managed_sql_session
from cleanstack.infrastructure.mongo import MongoDocument

type Context = MongoContext | SQLContext


@lru_cache
def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]


def get_sql_session(request: Request) -> Iterator[Session]:
    with managed_sql_session(request.app.state.sql_session_factory) as session:
        yield session


def get_mongo_session(request: Request) -> Iterator[ClientSession]:
    with managed_mongo_session(request.app.state.mongo_client) as session:
        yield session


def get_context(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    sql_session: Annotated[Session, Depends(get_sql_session)],
    mongo_session: Annotated[ClientSession, Depends(get_mongo_session)],
) -> Context:
    match settings.repository_type:
        case RepositoryType.MONGO:
            client: MongoClient[MongoDocument] = request.app.state.mongo_client
            return MongoContext(
                database=client[settings.mongo_database],
                session=mongo_session,
            )
        case RepositoryType.SQL:
            return SQLContext(session=sql_session)
