from collections.abc import Callable, Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.api.dependencies import get_settings
from app.core.settings import Settings


@pytest.fixture(scope="session")
def app(
    settings: Settings,
    settings_override_func: Callable[[], Settings],
) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = settings_override_func
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    # Use a context manager to ensure that the lifespan is called
    with TestClient(app) as client:
        yield client
