from collections.abc import Callable

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.api.dependencies.settings import get_settings
from app.core.config import Settings


@pytest.fixture(scope="session")
def app(
    settings: Settings,
    settings_override_func: Callable[[], Settings],
) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = settings_override_func
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
