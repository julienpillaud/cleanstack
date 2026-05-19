from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.entities import ItemStatus
from tests.plugins.database import ItemFactory


def test_operator_eq(
    item_factory: ItemFactory,
    client: TestClient,
) -> None:
    count = 2
    field = ItemStatus.ACTIVE
    item_factory.create_many(1, strenum_field=ItemStatus.INACTIVE)
    item_factory.create_many(count, strenum_field=field)

    params = {"filter": f"strenum_field={field}"}
    response = client.get("/items", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["items"]) == count
