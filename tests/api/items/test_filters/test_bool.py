import pytest
from fastapi import status
from httpx2 import AsyncClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_operator_eq(factory: Factory, client: AsyncClient) -> None:
    count = 2
    await factory.items.create_many(1, bool_field=True)
    await factory.items.create_many(count, bool_field=False)

    params = {"filter": "bool_field=false"}
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
    params = {"filter": f"bool_field[{operator}]=false"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}


@pytest.mark.anyio
async def test_wrong_value(client: AsyncClient) -> None:
    params = {"filter": "bool_field=bad"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
