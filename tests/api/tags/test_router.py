import uuid

import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.domain.items.repository import RepositoryType
from tests.api.tags import base_url


@pytest.mark.parametrize(
    "repository_type",
    [RepositoryType.DOCUMENT, RepositoryType.RELATIONAL],
)
def test_create_tag(
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    params = {"repository": repository_type}
    body = {"name": "test"}
    response = client.post(f"{base_url}", params=params, json=body)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert uuid.UUID(result["id"])
    assert result["name"] == "test"
