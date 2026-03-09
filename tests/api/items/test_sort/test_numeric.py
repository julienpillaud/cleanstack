import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.repository import RepositoryType
from cleanstack.entities import SortOrder
from tests.api.items import base_url
from tests.factories.items import ItemMongoFactory


@pytest.mark.parametrize(
    "field_name, values",
    [
        ("int_field", [1, 2, 3]),
        ("float_field", [1.1, 2.2, 3.3]),
    ],
)
@pytest.mark.parametrize(
    "direction, reverse",
    [
        (SortOrder.ASC, False),
        (SortOrder.DESC, True),
    ],
)
def test_sort_numeric(
    item_mongo_factory: ItemMongoFactory,
    client: TestClient,
    field_name: str,
    values: list[int | float],
    direction: SortOrder,
    reverse: bool,
) -> None:
    shuffled_values = [values[1], values[2], values[0]]
    for val in shuffled_values:
        item_mongo_factory.create_one(**{field_name: val})

    params = {
        "repository": RepositoryType.DOCUMENT,
        "sort": f"{field_name}[{direction}]",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    result_values = [item[field_name] for item in result["items"]]
    expected = sorted(values, reverse=reverse)
    assert result_values == expected
