from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.domain import get_domain
from app.domain.containers.entities import Container, ContainerCreate, ContainerUpdate
from app.domain.domain import Domain
from cleanstack.entities import EntityId

router = APIRouter(prefix="/containers", tags=["containers"])


@router.get("/{container_id}")
def get_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> Any:
    return domain.get_container(container_id=container_id)


@router.post("", response_model=Container, status_code=status.HTTP_201_CREATED)
def create_container(
    domain: Annotated[Domain, Depends(get_domain)],
    data: ContainerCreate,
) -> Any:
    return domain.create_container(data=data)


@router.patch("/{container_id}", response_model=Container)
def update_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
    data: ContainerUpdate,
) -> Any:
    return domain.update_container(container_id=container_id, data=data)


@router.delete("/{container_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_container(
    domain: Annotated[Domain, Depends(get_domain)],
    container_id: EntityId,
) -> None:
    domain.delete_container(container_id=container_id)
