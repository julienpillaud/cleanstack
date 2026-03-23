import uuid

from app.domain.context import ContextProtocol
from app.domain.items.repository import RepositoryType
from app.domain.tags.entities import Tag


def create_tag_command(
    context: ContextProtocol,
    /,
    name: str,
    repository: RepositoryType,
) -> Tag:
    tag = Tag(id=uuid.uuid7(), name=name)
    match repository:
        case RepositoryType.RELATIONAL:
            return context.tag_relational_repository.create(tag)
        case RepositoryType.DOCUMENT:
            return context.tag_document_repository.create(tag)
