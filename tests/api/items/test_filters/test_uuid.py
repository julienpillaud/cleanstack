import uuid

import pytest
from fastapi import status
from httpx2 import AsyncClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_operator_eq(
    factory: Factory,
    client: AsyncClient,
) -> None:
    count = 2
    field = uuid.uuid7()
    await factory.items.create_many(1)
    await factory.items.create_many(count, uuid_field=field)

    params = {"filter": f"uuid_field={field}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.anyio
async def test_operator_in(
    factory: Factory,
    client: AsyncClient,
) -> None:
    count = 2
    fields = (uuid.uuid7(), uuid.uuid7())
    await factory.items.create_many(1)
    await factory.items.create_many(1, uuid_field=fields[0])
    await factory.items.create_many(1, uuid_field=fields[1])

    params = {"filter": f"uuid_field[in]={fields[0]},{fields[1]}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.anyio
async def test_operator_not_in(
    factory: Factory,
    client: AsyncClient,
) -> None:
    count = 1
    fields = (uuid.uuid7(), uuid.uuid7())
    await factory.items.create_many(1)
    await factory.items.create_many(1, uuid_field=fields[0])
    await factory.items.create_many(1, uuid_field=fields[1])

    params = {"filter": f"uuid_field[nin]={fields[0]},{fields[1]}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.parametrize(
    "operator",
    (
        FilterOperator.LT,
        FilterOperator.LTE,
        FilterOperator.GTE,
        FilterOperator.GT,
    ),
)
@pytest.mark.anyio
async def test_unsupported_operator(
    client: AsyncClient,
    operator: FilterOperator,
) -> None:
    params = {"filter": f"uuid_field[{operator}]=test"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}


@pytest.mark.anyio
async def test_wrong_value(client: AsyncClient) -> None:
    params = {"filter": "uuid_field=bad"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
