import pytest
from fastapi import status
from httpx2 import AsyncClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


@pytest.mark.anyio
async def test_operator_in(factory: Factory, client: AsyncClient) -> None:
    count = 2
    await factory.items.create_many(1, int_field=1)
    await factory.items.create_many(1, int_field=2)
    await factory.items.create_many(1, int_field=3)

    params = {"filter": "int_field[in]=1,3"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.anyio
async def test_operator_nin(factory: Factory, client: AsyncClient) -> None:
    count = 1
    await factory.items.create_many(1, int_field=1)
    await factory.items.create_many(1, int_field=2)
    await factory.items.create_many(1, int_field=3)

    params = {"filter": "int_field[nin]=1,2"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.parametrize(
    "field_name, values, target_value",
    [
        ("int_field", [1, 2, 3], 2),
        ("float_field", [1.1, 2.1, 3.1], 2.1),
    ],
)
@pytest.mark.parametrize(
    "operator, expected_count",
    [
        (f"[{FilterOperator.LT}]", 1),
        (f"[{FilterOperator.LTE}]", 3),
        ("", 2),
        (f"[{FilterOperator.GTE}]", 6),
        (f"[{FilterOperator.GT}]", 4),
    ],
)
@pytest.mark.anyio
async def test_others_operators(
    factory: Factory,
    client: AsyncClient,
    field_name: str,
    values: list[int | float],
    target_value: int | float,
    operator: str,
    expected_count: int,
) -> None:
    await factory.items.create_many(1, **{field_name: values[0]})
    await factory.items.create_many(2, **{field_name: values[1]})
    await factory.items.create_many(4, **{field_name: values[2]})

    params = {"filter": f"{field_name}{operator}={target_value}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == expected_count


@pytest.mark.anyio
async def test_wrong_value(client: AsyncClient) -> None:
    params = {"filter": "int_field=bad"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}


@pytest.mark.anyio
async def test_computed_field(factory: Factory, client: AsyncClient) -> None:
    count = 1
    value = 2
    await factory.items.create_many(3, float_field=1)
    await factory.items.create_many(count, float_field=value)

    params = {"filter": f"computed_field={value * 2}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
