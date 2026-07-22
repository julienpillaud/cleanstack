from typing import Protocol

from app.domain.containers.entities import Container
from app.domain.protocols import AsyncRepositoryProtocol


class ContainerRepositoryProtocol(AsyncRepositoryProtocol[Container], Protocol): ...
