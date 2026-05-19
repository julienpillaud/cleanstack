from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import Context, get_context
from app.domain.containers.commands import (
    create_container_command,
    delete_container_command,
    get_container_command,
    update_container_command,
)
from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from cleanstack.entities import EntityId

router = APIRouter(prefix="/containers", tags=["containers"])


@router.get("/{container_id}")
def get_container(
    context: Annotated[Context, Depends(get_context)],
    container_id: EntityId,
) -> Any:
    return get_container_command(context, container_id=container_id)


@router.post("", response_model=Container, status_code=status.HTTP_201_CREATED)
def create_container(
    context: Annotated[Context, Depends(get_context)],
    data: ContainerCreate,
) -> Any:
    return create_container_command(context, data=data)


@router.patch("/{container_id}", response_model=Container)
def update_container(
    context: Annotated[Context, Depends(get_context)],
    container_id: EntityId,
    data: ContainerUpdate,
) -> Any:
    return update_container_command(context, container_id=container_id, data=data)


@router.delete("/{container_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_container(
    context: Annotated[Context, Depends(get_context)],
    container_id: EntityId,
) -> None:
    delete_container_command(context, container_id=container_id)
