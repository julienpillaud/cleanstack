from typing import Any

from pymongo.client_session import ClientSession
from pymongo.database import Database

from cleanstack.infrastructure.mongo.types import MongoDocument
from tests._app.domain.items.port import ItemRepositoryProtocol


class ItemRepository(ItemRepositoryProtocol):
    def __init__(
        self,
        database: Database[MongoDocument],
        session: ClientSession | None = None,
    ):
        self.database = database
        self.session = session

    def get(self) -> Any:
        return list(self.database["items"].find())
