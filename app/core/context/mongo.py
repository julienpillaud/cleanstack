from functools import cached_property

from app.core.domain import TransactionProtocol
from app.domain.containers.repository import ContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.mongo.containers import ContainerMongoRepository
from app.infrastructure.mongo.items import ItemMongoRepository
from app.infrastructure.mongo.utils import MongoTransaction


class MongoContext(ContextProtocol):
    def __init__(self, transaction: MongoTransaction) -> None:
        self.database = transaction.resource.database
        self.session = transaction.session

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(
            database=self.database,
            session=self.session,
        )

    @cached_property
    def container_repository(self) -> ContainerRepositoryProtocol:
        return ContainerMongoRepository(
            database=self.database,
            session=self.session,
        )


class MongoContextProvider:
    def __call__(self, transaction: TransactionProtocol) -> MongoContext:
        if not isinstance(transaction, MongoTransaction):
            raise RuntimeError()

        return MongoContext(transaction=transaction)
