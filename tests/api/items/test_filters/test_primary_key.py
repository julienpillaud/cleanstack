import uuid

import pytest
from fastapi import status
from httpx2 import AsyncClient

from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_operator_eq(
    factory: Factory,
    client: AsyncClient,
) -> None:
    count = 1
    item_id = uuid.uuid7()
    await factory.items.create_many(count, id=item_id)

    params = {"filter": f"id={item_id}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
