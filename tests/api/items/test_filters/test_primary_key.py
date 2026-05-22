import uuid

from fastapi import status
from fastapi.testclient import TestClient

from tests.plugins.factories import Factory


def test_operator_eq(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 1
    item_id = uuid.uuid7()
    factory.items.create_many(count, id=item_id)

    params = {"filter": f"id={item_id}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
