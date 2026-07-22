from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_domain
from app.core.domain import Domain
from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from app.domain.containers.use_cases import (
    create_container,
    delete_container,
    get_container,
    update_container,
)
from cleanstack import EntityId

router = APIRouter(prefix="/containers", tags=["containers"])


@router.get("/{container_id}")
async def get_container_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> Container:
    return await domain.run(get_container, container_id=container_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_container_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ContainerCreate,
) -> Container:
    return await domain.run(create_container, data=data)


@router.patch("/{container_id}")
async def update_container_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
    data: ContainerUpdate,
) -> Container:
    return await domain.run(update_container, container_id=container_id, data=data)


@router.delete("/{container_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_container_endpoint(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> None:
    await domain.run(delete_container, container_id=container_id)
