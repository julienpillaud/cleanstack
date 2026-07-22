import pytest
from fastapi import status
from httpx2 import AsyncClient

from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_search(
    factory: Factory,
    client: AsyncClient,
) -> None:
    total = 2
    await factory.items.create_many(3)
    string_field = "KeyWord In String Field"
    search = "keyword"
    await factory.items.create_many(total, string_field=string_field)

    params = {"search": search}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == total
    assert len(result["items"]) == total
    for item in result["items"]:
        assert search in item["string_field"].lower()


@pytest.mark.anyio
async def test_search_no_results(
    factory: Factory,
    client: AsyncClient,
) -> None:
    await factory.items.create_many(3)
    search = "nonexistent"

    params = {"search": search}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == 0
    assert len(result["items"]) == 0
