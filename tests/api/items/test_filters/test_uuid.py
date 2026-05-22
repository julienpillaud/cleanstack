import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cleanstack.entities import FilterOperator
from tests.plugins.factories import Factory


def test_operator_eq(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 2
    field = uuid.uuid7()
    factory.items.create_many(1)
    factory.items.create_many(count, uuid_field=field)

    params = {"filter": f"uuid_field={field}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_in(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 2
    fields = (uuid.uuid7(), uuid.uuid7())
    factory.items.create_many(1)
    factory.items.create_many(1, uuid_field=fields[0])
    factory.items.create_many(1, uuid_field=fields[1])

    params = {"filter": f"uuid_field[in]={fields[0]},{fields[1]}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_not_in(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 1
    fields = (uuid.uuid7(), uuid.uuid7())
    factory.items.create_many(1)
    factory.items.create_many(1, uuid_field=fields[0])
    factory.items.create_many(1, uuid_field=fields[1])

    params = {"filter": f"uuid_field[nin]={fields[0]},{fields[1]}"}
    response = client.get("/items", params=params)

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
def test_unsupported_operator(
    client: TestClient,
    operator: FilterOperator,
) -> None:
    params = {"filter": f"uuid_field[{operator}]=test"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}


def test_wrong_value(client: TestClient) -> None:
    params = {"filter": "uuid_field=bad"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
