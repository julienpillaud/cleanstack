from typing import Protocol

from app.domain.containers.entities import Container
from cleanstack.domain.repository import SyncRepositoryProtocol


class SyncContainerRepositoryProtocol(SyncRepositoryProtocol[Container], Protocol): ...
