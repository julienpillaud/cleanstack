from pymongo.client_session import ClientSession

from cleanstack.domain import UnitOfWorkProtocol
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from tests._app.domain.context import ContextProtocol
from tests._app.domain.items.port import ItemRepositoryProtocol
from tests._app.infrastructure.adapter import ItemRepository


class Context(ContextProtocol):
    def __init__(
        self,
        mongo_context: MongoContext,
        mongo_uow: MongoUnitOfWork | None = None,
    ):
        self.mongo_context = mongo_context
        self.mongo_uow = mongo_uow
        self.members = self._get_members()

    def _get_members(self) -> list[UnitOfWorkProtocol]:
        return [self.mongo_uow] if self.mongo_uow else []

    @property
    def _mongo_session(self) -> ClientSession | None:
        return self.mongo_uow.session if self.mongo_uow else None

    @property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )
