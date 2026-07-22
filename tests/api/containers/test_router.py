import pytest
from fastapi import status
from httpx2 import AsyncClient

from tests.plugins.factories import Factory
from tests.utils import assert_is_uuid


@pytest.mark.anyio
async def test_create_container(factory: Factory, client: AsyncClient) -> None:
    container = factory.containers.build()
    node_labels = [node.label for node in container.nodes]
    container_data = container.model_dump(exclude={"id", "nodes"})
    container_data["nodes"] = node_labels

    response = await client.post("/containers", json=container_data)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    container_id = result["id"]
    assert_is_uuid(container_id)
    assert result["name"] == container.name
    for node in result["nodes"]:
        assert_is_uuid(node["id"])
        assert node["label"] in node_labels

    get_response = await client.get(f"/containers/{container_id}")
    assert get_response.status_code == status.HTTP_200_OK
    get_result = get_response.json()
    assert get_result["id"] == container_id
    assert get_result["name"] == container.name
    for node in get_result["nodes"]:
        assert_is_uuid(node["id"])
        assert node["label"] in node_labels


@pytest.mark.anyio
async def test_update_container(
    factory: Factory,
    client: AsyncClient,
) -> None:
    container = await factory.containers.create_one()
    new_name = "New Container Name"

    response = await client.patch(
        f"/containers/{container.id}", json={"name": new_name}
    )

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["name"] == new_name

    get_response = await client.get(f"/containers/{container.id}")
    assert get_response.status_code == status.HTTP_200_OK
    get_result = get_response.json()
    assert get_result["name"] == new_name


@pytest.mark.parametrize(
    "initial_nodes, updated_nodes",
    [
        ([], ["label1"]),
        (["label1", "label2"], ["label1", "label2", "label3"]),
        (["label1", "label2"], ["label1"]),
        (["label1", "label2"], []),
        (["label1"], ["label2"]),
    ],
)
@pytest.mark.anyio
async def test_update_container_nodes(
    factory: Factory,
    client: AsyncClient,
    initial_nodes: list[str],
    updated_nodes: list[str],
) -> None:
    container = await factory.containers.create_one(nodes=initial_nodes)

    response = await client.patch(
        f"/containers/{container.id}", json={"nodes": updated_nodes}
    )
    assert response.status_code == status.HTTP_200_OK

    get_response = await client.get(f"/containers/{container.id}")
    assert get_response.status_code == status.HTTP_200_OK
    result = get_response.json()

    assert len(result["nodes"]) == len(updated_nodes)
    assert {node["label"] for node in result["nodes"]} == set(updated_nodes)


@pytest.mark.anyio
async def test_delete_container(factory: Factory, client: AsyncClient) -> None:
    container = await factory.containers.create_one()

    response = await client.delete(f"/containers/{container.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = await client.get(f"/containers/{container.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
