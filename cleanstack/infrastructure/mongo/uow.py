from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.database import Database

from cleanstack.domain.uow import UnitOfWorkProtocol
from cleanstack.infrastructure.mongo.logger import logger
from cleanstack.infrastructure.mongo.types import MongoDocument


class MongoContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: MongoClient[MongoDocument]
    database: Database[MongoDocument]

    @classmethod
    def from_settings(cls, host: str, database_name: str) -> MongoContext:
        logger.debug("Creating MongoDB client")
        client: MongoClient[MongoDocument] = MongoClient(
            host=host,
            uuidRepresentation="standard",
        )
        database = client[database_name]
        return cls(client=client, database=database)


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, context: MongoContext) -> None:
        self._session: ClientSession | None = None
        self.client = context.client

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("No active session")
        return self._session

    @contextmanager
    def transaction(self) -> Iterator[None]:
        logger.debug("Starting MongoDB session")
        self._session = self.client.start_session()
        self._session.start_transaction()
        try:
            yield
        finally:
            logger.debug("Closing MongoDB session")
            self._session.end_session()
            self._session = None

    def commit(self) -> None:
        self.session.commit_transaction()

    def rollback(self) -> None:
        self.session.abort_transaction()
