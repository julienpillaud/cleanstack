from typing import Annotated

from fastapi import Depends, HTTPException, Query, status

from app.api.filters import parse_filters
from app.api.sort import parse_sort_entities
from app.core.context import Context
from app.dependencies.fastapi.mongo import get_mongo_context, get_mongo_uow
from app.dependencies.fastapi.sql import get_sql_uow
from app.domain.domain import Domain
from cleanstack.domain import CompositeUniOfWork
from cleanstack.entities import FilterEntity, SortEntity
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork


def get_context(
    sql_uow: Annotated[SQLUnitOfWork, Depends(get_sql_uow)],
    mongo_context: Annotated[MongoContext, Depends(get_mongo_context)],
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
) -> Context:
    return Context(
        sql_uow=sql_uow,
        mongo_context=mongo_context,
        mongo_uow=mongo_uow,
    )


def get_domain(context: Annotated[Context, Depends(get_context)]) -> Domain:
    uow = CompositeUniOfWork(members=context.members)
    return Domain(uow=uow, context=context)


def get_filters(
    filters: Annotated[
        list[str] | None,
        Query(alias="filter"),
    ] = None,
) -> list[FilterEntity]:
    if not filters:
        return []

    try:
        return parse_filters(filters)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid filter format",
        ) from error


def get_sort_entities(
    sort_entities: Annotated[
        list[str] | None,
        Query(alias="sort"),
    ] = None,
) -> list[SortEntity]:
    if not sort_entities:
        return []

    try:
        return parse_sort_entities(sort_entities)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid sort format",
        ) from error


def get_search(search: str | None = None) -> str | None:
    return search
