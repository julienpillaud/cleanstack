from functools import cached_property

from app.core.protocols import UnitOfWorkProtocol
from app.domain.containers.repository import ContainerRepositoryProtocol
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.mongo.containers import ContainerMongoRepository
from app.infrastructure.mongo.items import ItemMongoRepository
from app.infrastructure.mongo.uow import MongoUnitOfWork


class MongoContext(ContextProtocol):
    def __init__(self, uow: MongoUnitOfWork) -> None:
        self.database = uow.resource.database
        self.session = uow.session

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
    def __call__(self, uow: UnitOfWorkProtocol) -> MongoContext:
        if not isinstance(uow, MongoUnitOfWork):
            raise RuntimeError()

        return MongoContext(uow=uow)
