from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.fastapi.dependencies import get_domain
from app.domain.domain import Domain
from app.domain.items.repository import RepositoryType
from app.domain.tags.entities import Tag, TagCreate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tag(
    domain: Annotated[Domain, Depends(get_domain)],
    repository: RepositoryType,
    tag_create: TagCreate,
) -> Tag:
    return domain.create_tag(repository=repository, name=tag_create.name)
