from typing import Any, Protocol


class ItemRepositoryProtocol(Protocol):
    def get(self) -> Any: ...
