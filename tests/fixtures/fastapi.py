import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.app import create_fastapi_app
from app.core.config import Settings
from app.dependencies.settings import get_settings
from tests.fixtures.settings import get_settings_override


@pytest.fixture(scope="session")
def app(settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=settings)
    app.dependency_overrides[get_settings] = get_settings_override
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
