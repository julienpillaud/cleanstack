import pytest
from fastapi.testclient import TestClient

from tests.fastapi.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
