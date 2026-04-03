from typing import Protocol

from app.domain.tags.entities import Tag
from cleanstack.domain.repository import SyncRepositoryProtocol


class TagRepositoryProtocol(SyncRepositoryProtocol[Tag], Protocol): ...
