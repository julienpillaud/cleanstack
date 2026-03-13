from typing import Protocol

from app.domain.tags.entities import Tag
from cleanstack.domain import RepositoryProtocol


class TagRepositoryProtocol(RepositoryProtocol[Tag], Protocol): ...
