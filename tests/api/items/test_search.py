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
def test_search(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    total = 2
    item_factory.create_many(3)
    string_field = "KeyWord In String Field"
    search = "keyword"
    item_factory.create_many(total, string_field=string_field)

    params = {
        "repository": repository_type,
        "search": search,
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total
    assert len(result["items"]) == total
    for item in result["items"]:
        assert search in item["string_field"].lower()


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_search_no_results(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    item_factory.create_many(3)
    search = "nonexistent"

    params = {
        "repository": repository_type,
        "search": search,
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == 0
    assert len(result["items"]) == 0
