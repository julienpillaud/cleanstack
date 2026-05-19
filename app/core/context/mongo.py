from functools import cached_property

from pymongo.client_session import ClientSession
from pymongo.database import Database

from app.domain.containers.repository import SyncContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import SyncItemRepositoryProtocol
from app.infrastructure.mongo.containers import SyncContainerMongoRepository
from app.infrastructure.mongo.items import SyncItemMongoRepository
from cleanstack.infrastructure.mongo import MongoDocument


class MongoContext(ContextProtocol):
    def __init__(
        self,
        database: Database[MongoDocument],
        session: ClientSession | None = None,
    ) -> None:
        self.database = database
        self.session = session

    @cached_property
    def item_repository(self) -> SyncItemRepositoryProtocol:
        return SyncItemMongoRepository(
            database=self.database,
            session=self.session,
        )

    @cached_property
    def container_repository(self) -> SyncContainerRepositoryProtocol:
        return SyncContainerMongoRepository(
            database=self.database,
            session=self.session,
        )
