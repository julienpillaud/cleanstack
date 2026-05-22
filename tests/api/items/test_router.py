from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domain.items.entities import ItemStatus
from tests.plugins.factories import Factory
from tests.utils import assert_datetime, assert_uuid


def test_get_items(
    factory: Factory,
    client: TestClient,
) -> None:
    count = 3
    factory.items.create_many(count)

    response = client.get("/items")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["total"] == count
    assert len(result["items"]) == count


def test_get_item(
    factory: Factory,
    client: TestClient,
) -> None:
    item = factory.items.create_one()

    response = client.get(f"/items/{item.id}")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert_uuid(result["id"], item.id)
    assert_uuid(result["uuid_field"], item.uuid_field)
    assert result["string_field"] == item.string_field
    assert result["int_field"] == item.int_field
    assert result["float_field"] == item.float_field
    assert result["bool_field"] == item.bool_field
    assert_datetime(result["datetime_field"], item.datetime_field)
    assert result["strenum_field"] == item.strenum_field
    assert result["optional_field"] == item.optional_field
    assert result["computed_field"] == item.computed_field


def test_create_item(
    factory: Factory,
    client: TestClient,
) -> None:
    item = factory.items.build()
    item_data = item.model_dump(
        exclude={
            "id",
            "uuid_field",
            "datetime_field",
            "computed_field",
        }
    )

    response = client.post("/items", json=item_data)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    item_id = result["id"]
    assert result["string_field"] == item.string_field
    assert result["int_field"] == item.int_field
    assert result["float_field"] == item.float_field
    assert result["bool_field"] == item.bool_field
    assert result["strenum_field"] == item.strenum_field
    assert result["optional_field"] == item.optional_field
    assert result["computed_field"] == item.computed_field

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == status.HTTP_200_OK
    get_result = get_response.json()
    assert get_result["id"] == item_id


@pytest.mark.parametrize(
    "field, previous_value, new_value",
    [
        ("string_field", "old", "new"),
        ("int_field", 1, 2),
        ("float_field", 1.1, 1.2),
        ("bool_field", False, True),
        ("bool_field", True, False),
        ("strenum_field", ItemStatus.INACTIVE, ItemStatus.ACTIVE),
        ("optional_field", None, ItemStatus.ACTIVE),
        ("optional_field", ItemStatus.ACTIVE, None),
        ("optional_field", ItemStatus.ACTIVE, ItemStatus.INACTIVE),
    ],
)
def test_update_item(
    factory: Factory,
    client: TestClient,
    field: str,
    previous_value: Any,
    new_value: Any,
) -> None:
    item = factory.items.create_one(**{field: previous_value})

    response = client.patch(f"/items/{item.id}", json={field: new_value})

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result[field] == new_value

    get_response = client.get(f"/items/{item.id}")
    assert get_response.status_code == status.HTTP_200_OK
    get_result = get_response.json()
    assert get_result[field] == new_value


def test_delete_item(
    factory: Factory,
    client: TestClient,
) -> None:
    item = factory.items.create_one()

    response = client.delete(f"/items/{item.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/items/{item.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
