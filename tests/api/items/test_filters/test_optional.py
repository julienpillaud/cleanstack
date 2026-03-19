import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.entities import ItemStatus
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
    count = 2
    field = ItemStatus.ACTIVE
    item_factory.create_many(1, optional_field=ItemStatus.INACTIVE)
    item_factory.create_many(count, optional_field=field)

    params = {
        "repository": repository_type,
        "filter": f"optional_field={field}",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
