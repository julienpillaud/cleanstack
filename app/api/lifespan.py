import time
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger
from app.core.settings import AppEnvironment, Settings
from app.infrastructure.mongo.utils import MongoResource
from app.infrastructure.sql.utils import SQLResource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        start_time = time.perf_counter()

        app.state.sql_resource = await SQLResource.from_settings(settings)
        if settings.environment == AppEnvironment.DEVELOPMENT:
            await app.state.sql_resource.init()
        app.state.mongo_resource = await MongoResource.from_settings(settings)

        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Application startup complete ({duration:.2f} s)")

        yield

        await app.state.mongo_resource.release()
        await app.state.sql_resource.release()

        logger.info("Application shutdown complete")

    return lifespan
