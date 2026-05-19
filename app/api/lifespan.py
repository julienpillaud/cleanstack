import time
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.settings import Settings
from app.infrastructure.mongo.utils import create_mongo_resource
from app.infrastructure.sql.utils import create_sql_resource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        start_time = time.perf_counter()

        sql_resource = create_sql_resource(settings=settings)
        app.state.sql_engine = sql_resource.engine
        app.state.sql_session_factory = sql_resource.session_factory

        mongo_resource = create_mongo_resource(settings=settings)
        app.state.mongo_client = mongo_resource.client
        app.state.mongo_database = mongo_resource.database

        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Application startup complete ({duration:.2f} s)")

        yield

        mongo_resource.close()
        sql_resource.close()

        logger.info("Application shutdown complete")

    return lifespan
