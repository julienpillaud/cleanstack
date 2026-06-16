from typing import Protocol

from app.domain.containers.entities import Container
from app.domain.protocols import SyncRepositoryProtocol


class SyncContainerRepositoryProtocol(SyncRepositoryProtocol[Container], Protocol): ...
