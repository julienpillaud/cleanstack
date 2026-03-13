import datetime

import pytest
from fastapi import status
from starlette.testclient import TestClient

from app.domain.items.repository import RepositoryType
from cleanstack.entities import SortOrder
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
    "direction, expected_indices",
    [
        (SortOrder.ASC, [0, 1, 2]),
        (SortOrder.DESC, [2, 1, 0]),
    ],
)
def test_sort_datetime(
    item_factory: ItemFactory,
    client: TestClient,
    direction: str,
    expected_indices: list[int],
    repository_type: RepositoryType,
) -> None:
    base_time = datetime.datetime(2026, 1, 1, 12, 0, 0, tzinfo=datetime.UTC)
    dates = [
        base_time,
        base_time + datetime.timedelta(hours=1),
        base_time + datetime.timedelta(hours=2),
    ]
    item_factory.create_many(1, datetime_field=dates[1])
    item_factory.create_many(1, datetime_field=dates[2])
    item_factory.create_many(1, datetime_field=dates[0])

    params = {
        "repository": repository_type,
        "sort": f"datetime_field[{direction}]",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    expected_dates = [dates[i] for i in expected_indices]
    result_dates = [
        datetime.datetime.fromisoformat(item["datetime_field"])
        for item in result["items"]
    ]
    assert result_dates == expected_dates
