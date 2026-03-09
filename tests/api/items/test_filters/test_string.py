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
def test_operator_eq(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 2
    field = "included"
    item_factory.create_many(1, string_field="excluded")
    item_factory.create_many(count, string_field=field)

    params = {
        "repository": repository_type,
        "filter": f"string_field={field}",
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
def test_operator_in(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 2
    fields = ("included1", "included2")
    item_factory.create_many(1, string_field="excluded")
    item_factory.create_many(1, string_field=fields[0])
    item_factory.create_many(1, string_field=fields[1])

    params = {
        "repository": repository_type,
        "filter": f"string_field[in]={','.join(fields)}",
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
def test_operator_not_in(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    count = 1
    fields = ("excluded1", "excluded2")
    item_factory.create_many(1, string_field="excluded1")
    item_factory.create_many(1, string_field="excluded2")
    item_factory.create_many(1, string_field="included")

    params = {
        "repository": repository_type,
        "filter": f"string_field[nin]={','.join(fields)}",
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
    repository_type: RepositoryType,
) -> None:
    params = {
        "repository": repository_type,
        "filter": f"string_field[{operator}]=test",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}
