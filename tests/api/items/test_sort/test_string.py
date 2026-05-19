import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cleanstack.entities import SortOrder
from tests.plugins.database import ItemFactory


@pytest.mark.parametrize(
    "direction, expected",
    [
        (SortOrder.ASC, ["Alice", "Bob", "Charlie"]),
        (SortOrder.DESC, ["Charlie", "Bob", "Alice"]),
    ],
)
def test_sort_string(
    item_factory: ItemFactory,
    client: TestClient,
    direction: str,
    expected: list[str],
) -> None:
    for name in ["Bob", "Charlie", "Alice"]:
        item_factory.create_one(string_field=name)

    params = {"sort": f"string_field[{direction}]"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()

    names = [item["string_field"] for item in result["items"]]
    assert names == expected
