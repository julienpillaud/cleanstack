from fastapi import status
from fastapi.testclient import TestClient

from tests.plugins.factories import Factory


def test_pagination_request_less_than_total(
    factory: Factory,
    client: TestClient,
) -> None:
    page = 1
    size = 5
    total = 9
    factory.items.create_many(total)

    params: dict[str, str | int] = {
        "page": page,
        "size": size,
    }
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == size


def test_pagination_request_more_than_total(
    factory: Factory,
    client: TestClient,
) -> None:
    page = 2
    size = 5
    total = 9
    factory.items.create_many(total)

    params: dict[str, str | int] = {
        "page": page,
        "size": size,
    }
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == total - size


def test_pagination_out_of_range(
    factory: Factory,
    client: TestClient,
) -> None:
    page = 3
    size = 5
    total = 9
    factory.items.create_many(total)

    params: dict[str, str | int] = {
        "page": page,
        "size": size,
    }
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["page"] == page
    assert result["size"] == size
    assert result["total"] == total
    assert len(result["items"]) == 0
