from typing import Protocol

from app.domain.items.entities import Item
from app.domain.protocols import AsyncRepositoryProtocol


class ItemRepositoryProtocol(AsyncRepositoryProtocol[Item], Protocol): ...
