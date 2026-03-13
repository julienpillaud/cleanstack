import uuid
from typing import Any

from faker import Faker

from app.domain.tags.entities import Tag
from app.infrastructure.mongo.tags import TagMongoRepository
from app.infrastructure.sql.tags import TagSQLRepository
from cleanstack.factories import BaseMongoFactory, BaseSQLFactory


def generate_tag(faker: Faker, **kwargs: Any) -> Tag:
    return Tag(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        name=kwargs["name"] if "name" in kwargs else faker.name(),
    )


class TagMongoFactory(BaseMongoFactory[Tag]):
    def build(self, **kwargs: Any) -> Tag:
        return generate_tag(faker=self.faker, **kwargs)

    @property
    def _repository(self) -> TagMongoRepository:
        return TagMongoRepository(
            database=self.context.database,
            session=self.uow.session,
        )


class TagSQLFactory(BaseSQLFactory[Tag]):
    def build(self, **kwargs: Any) -> Tag:
        return generate_tag(faker=self.faker, **kwargs)

    @property
    def _repository(self) -> TagSQLRepository:
        return TagSQLRepository(session=self.uow.session)
