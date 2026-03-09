import datetime

import pytest
from fastapi.testclient import TestClient
from starlette import status

from app.domain.items.repository import RepositoryType
from cleanstack.entities import FilterOperator
from tests.api.items import base_url
from tests.factories.items import ItemFactory


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
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
def test_comparison_operators(
    item_factory: ItemFactory,
    client: TestClient,
    operator: str,
    expected_count: int,
    repository_type: RepositoryType,
) -> None:
    item_factory.create_many(1, datetime_field=datetime.datetime(2026, 1, 1, 8, 0))
    item_factory.create_many(2, datetime_field=datetime.datetime(2026, 1, 1, 12, 0))
    item_factory.create_many(4, datetime_field=datetime.datetime(2026, 1, 1, 20, 0))

    target = "2026-01-01T12:00:00"
    op_suffix = f"[{operator}]" if operator != FilterOperator.EQ else ""
    params = {
        "repository": repository_type,
        "filter": f"datetime_field{op_suffix}={target}",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == expected_count


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_wrong_value(client: TestClient, repository_type: RepositoryType) -> None:
    params = {
        "repository": repository_type,
        "filter": "datetime_field=bad",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
