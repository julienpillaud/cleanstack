from fastapi import status
from fastapi.testclient import TestClient

from tests.plugins.database import ItemFactory


def test_search(
    item_factory: ItemFactory,
    client: TestClient,
) -> None:
    total = 2
    item_factory.create_many(3)
    string_field = "KeyWord In String Field"
    search = "keyword"
    item_factory.create_many(total, string_field=string_field)

    params = {"search": search}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total
    assert len(result["items"]) == total
    for item in result["items"]:
        assert search in item["string_field"].lower()


def test_search_no_results(
    item_factory: ItemFactory,
    client: TestClient,
) -> None:
    item_factory.create_many(3)
    search = "nonexistent"

    params = {"search": search}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == 0
    assert len(result["items"]) == 0
