import pytest
from fastapi import status
from fastapi.testclient import TestClient

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
def test_operator_in(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 2
    item_factory.create_many(1, int_field=1)
    item_factory.create_many(1, int_field=2)
    item_factory.create_many(1, int_field=3)

    params = {
        "repository": repository_type,
        "filter": "int_field[in]=1,3",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_operator_nin(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 1
    item_factory.create_many(1, int_field=1)
    item_factory.create_many(1, int_field=2)
    item_factory.create_many(1, int_field=3)

    params = {
        "repository": repository_type,
        "filter": "int_field[nin]=1,2",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
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
def test_others_operators(
    item_factory: ItemFactory,
    client: TestClient,
    field_name: str,
    values: list[int | float],
    target_value: int | float,
    operator: str,
    expected_count: int,
    repository_type: RepositoryType,
) -> None:
    item_factory.create_many(1, **{field_name: values[0]})
    item_factory.create_many(2, **{field_name: values[1]})
    item_factory.create_many(4, **{field_name: values[2]})

    params = {
        "repository": repository_type,
        "filter": f"{field_name}{operator}={target_value}",
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
        "filter": "int_field=bad",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_computed_field(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 1
    value = 2
    item_factory.create_many(3, float_field=1)
    item_factory.create_many(count, float_field=value)

    params = {
        "repository": repository_type,
        "filter": f"computed_field={value * 2}",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
