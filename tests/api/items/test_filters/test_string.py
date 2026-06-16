import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cleanstack import FilterOperator
from tests.plugins.factories import Factory


def test_operator_eq(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 2
    field = "included"
    factory.items.create_many(1, string_field="excluded")
    factory.items.create_many(count, string_field=field)

    params = {"filter": f"string_field={field}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_in(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 2
    fields = ("included1", "included2")
    factory.items.create_many(1, string_field="excluded")
    factory.items.create_many(1, string_field=fields[0])
    factory.items.create_many(1, string_field=fields[1])

    params = {"filter": f"string_field[in]={','.join(fields)}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count


def test_operator_not_in(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 1
    fields = ("excluded1", "excluded2")
    factory.items.create_many(1, string_field="excluded1")
    factory.items.create_many(1, string_field="excluded2")
    factory.items.create_many(1, string_field="included")

    params = {"filter": f"string_field[nin]={','.join(fields)}"}
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
    params = {"filter": f"string_field[{operator}]=test"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}
