import pytest
from fastapi import status
from httpx2 import AsyncClient

from app.domain.items.entities import ItemStatus
from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_operator_eq(
    factory: Factory,
    client: AsyncClient,
) -> None:
    count = 2
    field = ItemStatus.ACTIVE
    await factory.items.create_many(1, optional_field=ItemStatus.INACTIVE)
    await factory.items.create_many(count, optional_field=field)

    params = {"filter": f"optional_field={field}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
