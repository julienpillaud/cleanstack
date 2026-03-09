from typing import Protocol

from app.domain.items.repository import ItemRepositoryProtocol
from cleanstack.domain import BaseContextProtocol


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def item_relational_repository(self) -> ItemRepositoryProtocol: ...

    @property
    def item_document_repository(self) -> ItemRepositoryProtocol: ...
