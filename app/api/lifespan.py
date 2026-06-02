import time
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.settings import Settings
from app.infrastructure.mongo.utils import MongoResource
from app.infrastructure.sql.utils import SQLResource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        start_time = time.perf_counter()

        sql_resource = SQLResource.from_settings(settings)
        app.state.sql_resource = sql_resource

        mongo_resource = MongoResource.from_settings(settings)
        app.state.mongo_resource = mongo_resource

        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Application startup complete ({duration:.2f} s)")

        yield

        mongo_resource.release()
        sql_resource.release()

        logger.info("Application shutdown complete")

    return lifespan
