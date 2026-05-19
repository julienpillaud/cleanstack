import uuid
from typing import Any

from app.domain.items.entities import Item, ItemStatus
from app.infrastructure.mongo.items import SyncItemMongoRepository
from app.infrastructure.sql.items import SyncItemSQLRepository
from cleanstack.factories.mongo import BaseMongoFactory
from cleanstack.factories.sql import BaseSQLFactory
from tests.factories.utils import faker


def generate_item(**kwargs: Any) -> Item:
    return Item(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        uuid_field=kwargs.get("uuid_field", uuid.uuid7()),
        string_field=kwargs.get("string_field", faker.random_string()),
        int_field=kwargs.get("int_field", faker.random_int()),
        float_field=kwargs.get("float_field", faker.random_float()),
        bool_field=kwargs.get("bool_field", faker.random_bool()),
        datetime_field=kwargs.get("datetime_field", faker.random_datetime()),
        strenum_field=kwargs.get("strenum_field", faker.choice(list(ItemStatus))),
        optional_field=kwargs.get(
            "optional_field",
            faker.optional_choice(list(ItemStatus)),
        ),
    )


class ItemMongoFactory(BaseMongoFactory[Item]):
    def build(self, **kwargs: Any) -> Item:
        return generate_item(**kwargs)

    @property
    def _repository(self) -> SyncItemMongoRepository:
        return SyncItemMongoRepository(database=self.database)


class ItemSQLFactory(BaseSQLFactory[Item]):
    def build(self, **kwargs: Any) -> Item:
        return generate_item(**kwargs)

    @property
    def _repository(self) -> SyncItemSQLRepository:
        return SyncItemSQLRepository(session=self.session)
