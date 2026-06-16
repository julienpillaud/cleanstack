import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


def test_operator_eq(factory: Factory, client: TestClient) -> None:
    count = 2
    factory.items.create_many(1, bool_field=True)
    factory.items.create_many(count, bool_field=False)

    params = {"filter": "bool_field=false"}
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
    params = {"filter": f"bool_field[{operator}]=false"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}


def test_wrong_value(client: TestClient) -> None:
    params = {"filter": "bool_field=bad"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
