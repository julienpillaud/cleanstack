import pytest
from fastapi import status
from httpx2 import AsyncClient

from cleanstack import SortOrder
from tests.plugins.factories import Factory


@pytest.mark.parametrize(
    "direction, expected",
    [
        (SortOrder.ASC, ["Alice", "Bob", "Charlie"]),
        (SortOrder.DESC, ["Charlie", "Bob", "Alice"]),
    ],
)
@pytest.mark.anyio
async def test_sort_string(
    factory: Factory,
    client: AsyncClient,
    direction: str,
    expected: list[str],
) -> None:
    for name in ["Bob", "Charlie", "Alice"]:
        await factory.items.create_one(string_field=name)

    params = {"sort": f"string_field[{direction}]"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()

    names = [item["string_field"] for item in result["items"]]
    assert names == expected
