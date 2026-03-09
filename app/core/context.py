from pymongo.client_session import ClientSession

from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.mongo.items import ItemMongoRepository
from app.infrastructure.sql.items import ItemSQLRepository
from cleanstack.domain import UnitOfWorkProtocol
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork


class Context(ContextProtocol):
    def __init__(
        self,
        sql_uow: SQLUnitOfWork,
        mongo_context: MongoContext,
        mongo_uow: MongoUnitOfWork | None = None,
    ):
        self.sql_uow = sql_uow
        self.mongo_context = mongo_context
        self.mongo_uow = mongo_uow
        self.members = self._get_members()

    def _get_members(self) -> list[UnitOfWorkProtocol]:
        members: list[UnitOfWorkProtocol] = [self.sql_uow]
        if self.mongo_uow:
            members.append(self.mongo_uow)
        return members

    @property
    def _mongo_session(self) -> ClientSession | None:
        return self.mongo_uow.session if self.mongo_uow else None

    @property
    def item_relational_repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.sql_uow.session)

    @property
    def item_document_repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )
