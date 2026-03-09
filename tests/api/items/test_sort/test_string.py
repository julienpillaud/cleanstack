import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.repository import RepositoryType
from cleanstack.entities import SortOrder
from tests.api.items import base_url
from tests.factories.items import ItemMongoFactory


@pytest.mark.parametrize(
    "direction, expected",
    [
        (SortOrder.ASC, ["Alice", "Bob", "Charlie"]),
        (SortOrder.DESC, ["Charlie", "Bob", "Alice"]),
    ],
)
def test_sort_string(
    item_mongo_factory: ItemMongoFactory,
    client: TestClient,
    direction: str,
    expected: list[str],
) -> None:
    for name in ["Bob", "Charlie", "Alice"]:
        item_mongo_factory.create_one(string_field=name)

    params = {
        "repository": RepositoryType.DOCUMENT,
        "sort": f"string_field[{direction}]",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()

    names = [item["string_field"] for item in result["items"]]
    assert names == expected
