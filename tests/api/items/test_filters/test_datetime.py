import datetime

import pytest
from fastapi import status
from httpx2 import AsyncClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


@pytest.mark.parametrize(
    "operator, expected_count",
    [
        (FilterOperator.LT, 1),  # 08:00
        (FilterOperator.LTE, 3),  # 08:00 + 12:00
        (FilterOperator.EQ, 2),  # 12:00
        (FilterOperator.GTE, 6),  # 12:00 + 20:00
        (FilterOperator.GT, 4),  # 20:00
    ],
)
@pytest.mark.anyio
async def test_comparison_operators(
    factory: Factory,
    client: AsyncClient,
    operator: str,
    expected_count: int,
) -> None:
    await factory.items.create_many(
        1, datetime_field=datetime.datetime(2026, 1, 1, 8, 0)
    )
    await factory.items.create_many(
        2, datetime_field=datetime.datetime(2026, 1, 1, 12, 0)
    )
    await factory.items.create_many(
        4, datetime_field=datetime.datetime(2026, 1, 1, 20, 0)
    )

    target = "2026-01-01T12:00:00"
    op_suffix = f"[{operator}]" if operator != FilterOperator.EQ else ""
    params = {"filter": f"datetime_field{op_suffix}={target}"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == expected_count


@pytest.mark.anyio
async def test_wrong_value(
    client: AsyncClient,
) -> None:
    params = {"filter": "datetime_field=bad"}
    response = await client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
