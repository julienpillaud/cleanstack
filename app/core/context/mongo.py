from app.domain.context import ContextProtocol
from app.domain.items.repository import SyncItemRepositoryProtocol
from app.infrastructure.mongo.items import SyncItemMongoRepository
from cleanstack.domain import UnitOfWorkProtocol
from cleanstack.infrastructure.mongo import MongoUnitOfWork


class MongoContext(ContextProtocol):
    def __init__(self, mongo_uow: MongoUnitOfWork):
        self.mongo_uow = mongo_uow
        self.members: list[UnitOfWorkProtocol] = [self.mongo_uow]

    @property
    def item_repository(self) -> SyncItemRepositoryProtocol:
        return SyncItemMongoRepository(
            database=self.mongo_uow.database,
            session=self.mongo_uow.session,
        )
