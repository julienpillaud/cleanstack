import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.repository import RepositoryType
from tests.api.items import base_url
from tests.factories.items import ItemFactory


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_operator_eq(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 1
    item_id = uuid.uuid7()
    item_factory.create_many(count, id=item_id)

    params = {
        "repository": repository_type,
        "filter": f"id={item_id}",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
