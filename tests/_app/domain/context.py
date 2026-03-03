from typing import Protocol

from cleanstack.domain import BaseContextProtocol
from tests._app.domain.items.port import ItemRepositoryProtocol


class ContextProtocol(BaseContextProtocol, Protocol):
    @property
    def item_repository(self) -> ItemRepositoryProtocol: ...
