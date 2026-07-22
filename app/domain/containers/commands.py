import uuid

from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from app.domain.context import ContextProtocol
from app.domain.exceptions import NotFoundError
from app.domain.nodes.entities import Node
from cleanstack import EntityId


async def get_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
) -> Container:
    container = await context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    return container


async def create_container_command(
    context: ContextProtocol,
    /,
    data: ContainerCreate,
) -> Container:
    container = Container(
        id=uuid.uuid7(),
        name=data.name,
        nodes=[Node(id=uuid.uuid7(), label=tag) for tag in data.nodes],
    )
    await context.container_repository.save(container)
    return container


async def update_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
    data: ContainerUpdate,
) -> Container:
    container = await context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if key == "nodes":
            container.nodes = [Node(id=uuid.uuid7(), label=tag) for tag in value]
            continue
        setattr(container, key, value)

    await context.container_repository.update(container)
    return container


async def delete_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
) -> None:
    container = await context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    await context.container_repository.remove(container)
