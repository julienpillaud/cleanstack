import datetime
import random
import uuid
from typing import Any

from faker import Faker

from app.domain.items.entities import Item
from app.infrastructure.mongo.items import ItemMongoRepository
from app.infrastructure.sql.items import ItemSQLRepository
from cleanstack.factories import BaseMongoFactory, BaseSQLFactory
from tests.factories.tags import TagMongoFactory, TagSQLFactory


def generate_item(faker: Faker, **kwargs: Any) -> Item:
    return Item(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        uuid_field=kwargs["uuid_field"] if "uuid_field" in kwargs else uuid.uuid7(),
        string_field=kwargs["string_field"]
        if "string_field" in kwargs
        else faker.name(),
        int_field=kwargs["int_field"] if "int_field" in kwargs else faker.pyint(),
        float_field=kwargs["float_field"]
        if "float_field" in kwargs
        else faker.pyfloat(),
        bool_field=kwargs["bool_field"] if "bool_field" in kwargs else faker.pybool(),
        datetime_field=kwargs["datetime_field"]
        if "datetime_field" in kwargs
        else datetime.datetime.now(datetime.UTC),
        optional_field=kwargs["optional_field"]
        if "optional_field" in kwargs
        else (faker.name() if faker.pybool() else None),
        tags=kwargs["tags"],
    )


class ItemMongoFactory(BaseMongoFactory[Item]):
    @property
    def tag_factory(self) -> TagMongoFactory:
        return TagMongoFactory(faker=self.faker, context=self.context)

    def build(self, **kwargs: Any) -> Item:
        if "tags" not in kwargs:
            kwargs["tags"] = self.tag_factory.create_many(random.randint(1, 3))
        return generate_item(faker=self.faker, **kwargs)

    @property
    def _repository(self) -> ItemMongoRepository:
        return ItemMongoRepository(
            database=self.context.database,
            session=self.uow.session,
        )


class ItemSQLFactory(BaseSQLFactory[Item]):
    @property
    def tag_factory(self) -> TagSQLFactory:
        return TagSQLFactory(faker=self.faker, context=self.context)

    def build(self, **kwargs: Any) -> Item:
        if "tags" not in kwargs:
            kwargs["tags"] = self.tag_factory.create_many(random.randint(1, 3))
        return generate_item(faker=self.faker, **kwargs)

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
