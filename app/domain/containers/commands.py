import uuid

from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from app.domain.context import ContextProtocol
from app.domain.nodes.entities import Node
from cleanstack.domain import NotFoundError
from cleanstack.entities import EntityId


def get_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
) -> Container:
    container = context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    return container


def create_container_command(
    context: ContextProtocol,
    /,
    data: ContainerCreate,
) -> Container:
    container = Container(
        id=uuid.uuid7(),
        name=data.name,
        nodes=[Node(id=uuid.uuid7(), label=tag) for tag in data.nodes],
    )
    context.container_repository.save(container)
    return container


def update_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
    data: ContainerUpdate,
) -> Container:
    container = context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        if key == "nodes":
            container.nodes = [Node(id=uuid.uuid7(), label=tag) for tag in value]
            continue
        setattr(container, key, value)

    context.container_repository.update(container)
    return container


def delete_container_command(
    context: ContextProtocol,
    /,
    container_id: EntityId,
) -> None:
    container = context.container_repository.get_by_id(container_id)
    if not container:
        raise NotFoundError("Container not found")

    context.container_repository.remove(container)
