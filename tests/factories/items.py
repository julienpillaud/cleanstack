import random
import uuid
from typing import Any

from app.domain.items.entities import Item, ItemStatus
from app.infrastructure.mongo.items import SyncItemMongoRepository
from app.infrastructure.sql.items import ItemSQLRepository
from cleanstack.factories.mongo import BaseMongoFactory
from cleanstack.factories.sql import BaseSQLFactory
from tests.factories.tags import TagMongoFactory, TagSQLFactory
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
        tags=kwargs.get("tags", []),
    )


class ItemMongoFactory(BaseMongoFactory[Item]):
    @property
    def tag_factory(self) -> TagMongoFactory:
        return TagMongoFactory(context=self.context)

    def build(self, **kwargs: Any) -> Item:
        if "tags" not in kwargs:
            kwargs["tags"] = self.tag_factory.create_many(random.randint(1, 3))
        return generate_item(**kwargs)

    @property
    def _repository(self) -> SyncItemMongoRepository:
        return SyncItemMongoRepository(
            database=self.context.database,
            session=self.uow.session,
        )


class ItemSQLFactory(BaseSQLFactory[Item]):
    @property
    def tag_factory(self) -> TagSQLFactory:
        return TagSQLFactory(context=self.context)

    def build(self, **kwargs: Any) -> Item:
        if "tags" not in kwargs:
            kwargs["tags"] = self.tag_factory.create_many(random.randint(1, 3))
        return generate_item(**kwargs)

    @property
    def _repository(self) -> ItemSQLRepository:
        return ItemSQLRepository(session=self.uow.session)


class ItemFactory:
    def __init__(
        self,
        mongo_factory: ItemMongoFactory,
        sql_factory: ItemSQLFactory,
    ) -> None:
        self.mongo_factory = mongo_factory
        self.sql_factory = sql_factory

    def create_many(self, count: int, /, **kwargs: Any) -> None:
        entities = [self.mongo_factory.build(**kwargs) for _ in range(count)]

        with self.mongo_factory._persistence_context():
            for entity in entities:
                self.mongo_factory._repository.create(entity)
            self.mongo_factory._commit()

        with self.sql_factory._persistence_context():
            for entity in entities:
                self.sql_factory._repository.create(entity)
            self.sql_factory._commit()
