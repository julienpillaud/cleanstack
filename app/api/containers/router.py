from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain
from app.core.domain import Domain
from app.domain.containers.commands import (
    create_container_command,
    delete_container_command,
    get_container_command,
    update_container_command,
)
from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from cleanstack import EntityId

router = APIRouter(prefix="/containers", tags=["containers"])


@router.get("/{container_id}")
async def get_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> Container:
    return await domain.run(get_container_command, container_id=container_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_container(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ContainerCreate,
) -> Container:
    return await domain.run(create_container_command, data=data)


@router.patch("/{container_id}")
async def update_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
    data: ContainerUpdate,
) -> Container:
    return await domain.run(
        update_container_command, container_id=container_id, data=data
    )


@router.delete("/{container_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> None:
    await domain.run(delete_container_command, container_id=container_id)
