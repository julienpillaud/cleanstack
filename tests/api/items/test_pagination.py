import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.repository import RepositoryType
from tests.api.items import base_url
from tests.factories.items import ItemFactory


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_pagination_request_less_than_total(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    page = 1
    size = 5
    total = 9
    item_factory.create_many(total)

    params: dict[str, str | int] = {
        "repository": repository_type,
        "page": page,
        "size": size,
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == size


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_pagination_request_more_than_total(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    page = 2
    size = 5
    total = 9
    item_factory.create_many(total)

    params: dict[str, str | int] = {
        "repository": repository_type,
        "page": page,
        "size": size,
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == total - size


@pytest.mark.parametrize(
    "repository_type",
    [
        RepositoryType.DOCUMENT,
        RepositoryType.RELATIONAL,
    ],
)
def test_pagination_out_of_range(
    item_factory: ItemFactory,
    client: TestClient,
    repository_type: RepositoryType,
) -> None:
    page = 3
    size = 5
    total = 9
    item_factory.create_many(total)

    params: dict[str, str | int] = {
        "repository": repository_type,
        "page": page,
        "size": size,
    }
    response = client.get(base_url, params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == 0
