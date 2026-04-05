from typing import Protocol

from app.domain.items.repository import SyncItemRepositoryProtocol
from app.domain.tags.repository import TagRepositoryProtocol
from cleanstack.domain import BaseContextProtocol


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def item_relational_repository(self) -> SyncItemRepositoryProtocol: ...

    @property
    def item_document_repository(self) -> SyncItemRepositoryProtocol: ...

    @property
    def tag_relational_repository(self) -> TagRepositoryProtocol: ...

    @property
    def tag_document_repository(self) -> TagRepositoryProtocol: ...
