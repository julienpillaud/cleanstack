import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cleanstack import SortOrder
from tests.plugins.factories import Factory


@pytest.mark.parametrize(
    "direction, expected",
    [
        (SortOrder.ASC, ["Alice", "Bob", "Charlie"]),
        (SortOrder.DESC, ["Charlie", "Bob", "Alice"]),
    ],
)
def test_sort_string(
    factory: Factory,
    client: TestClient,
    direction: str,
    expected: list[str],
) -> None:
    for name in ["Bob", "Charlie", "Alice"]:
        factory.items.create_one(string_field=name)

    params = {"sort": f"string_field[{direction}]"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()

    names = [item["string_field"] for item in result["items"]]
    assert names == expected
