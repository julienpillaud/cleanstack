import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest import FixtureRequest

from app.domain.items.repository import RepositoryType
from tests.api.items import base_url


@pytest.mark.parametrize(
    "factory_name, repository_type",
    [
        ("item_mongo_factory", RepositoryType.DOCUMENT),
        ("item_sql_factory", RepositoryType.RELATIONAL),
    ],
)
def test_get_item(
    client: TestClient,
    factory_name: str,
    repository_type: RepositoryType,
    request: FixtureRequest,
) -> None:
    factory = request.getfixturevalue(factory_name)
    item = factory.create_one()
    tags = sorted(item.tags, key=lambda x: x.id)

    params = {"repository": repository_type}
    response = client.get(f"{base_url}/{item.id}", params=params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(item.id)
    assert result["uuid_field"] == str(item.uuid_field)
    assert result["string_field"] == item.string_field
    assert result["int_field"] == item.int_field
    assert result["float_field"] == item.float_field
    assert result["bool_field"] == item.bool_field
    assert (
        datetime.datetime.fromisoformat(result["datetime_field"]) == item.datetime_field
    )
    assert result["strenum_field"] == item.strenum_field
    assert result["optional_field"] == item.optional_field
    assert result["computed_field"] == item.computed_field

    result_tags = sorted(result["tags"], key=lambda x: x["id"])
    assert len(result_tags) == len(tags)
    for tag, result_tag in zip(tags, result_tags, strict=True):
        assert result_tag["id"] == str(tag.id)
        assert result_tag["name"] == tag.name
