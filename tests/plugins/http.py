from collections.abc import AsyncIterator, Callable

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient
from starlette.types import ASGIApp

from app.api.app import create_fastapi_app
from app.api.dependencies import get_settings
from app.core.settings import Settings


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def app(
    settings: Settings,
    settings_override_func: Callable[[], Settings],
) -> AsyncIterator[ASGIApp]:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = settings_override_func
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
