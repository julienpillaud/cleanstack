import uuid

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
    field = uuid.uuid7()
    item_factory.create_many(1)
    item_factory.create_many(count, uuid_field=field)

    params = {
        "repository": repository_type,
        "filter": f"uuid_field={field}",
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
    fields = (uuid.uuid7(), uuid.uuid7())
    item_factory.create_many(1)
    item_factory.create_many(1, uuid_field=fields[0])
    item_factory.create_many(1, uuid_field=fields[1])

    params = {
        "repository": repository_type,
        "filter": f"uuid_field[in]={fields[0]},{fields[1]}",
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
    fields = (uuid.uuid7(), uuid.uuid7())
    item_factory.create_many(
        1,
    )
    item_factory.create_many(1, uuid_field=fields[0])
    item_factory.create_many(1, uuid_field=fields[1])

    params = {
        "repository": repository_type,
        "filter": f"uuid_field[nin]={fields[0]},{fields[1]}",
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
        "filter": f"uuid_field[{operator}]=test",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Unsupported operator"}


def test_wrong_value(client: TestClient) -> None:
    params = {
        "repository": RepositoryType.DOCUMENT,
        "filter": "uuid_field=bad",
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    result = response.json()
    assert result == {"detail": "Invalid value format"}
