import uuid
from typing import Any

from app.domain.tags.entities import Tag
from app.infrastructure.mongo.tags import TagMongoRepository
from app.infrastructure.sql.tags import TagSQLRepository
from cleanstack.factories.mongo import BaseMongoFactory
from cleanstack.factories.sql import BaseSQLFactory
from tests.factories.utils import faker


def generate_tag(**kwargs: Any) -> Tag:
    return Tag(
        id=kwargs.get("id", uuid.uuid7()),
        name=kwargs.get("name", faker.random_string()),
    )


class TagMongoFactory(BaseMongoFactory[Tag]):
    def build(self, **kwargs: Any) -> Tag:
        return generate_tag(**kwargs)

    @property
    def _repository(self) -> TagMongoRepository:
        return TagMongoRepository(
            database=self.context.database,
            session=self.uow.session,
        )


class TagSQLFactory(BaseSQLFactory[Tag]):
    def build(self, **kwargs: Any) -> Tag:
        return generate_tag(**kwargs)

    @property
    def _repository(self) -> TagSQLRepository:
        return TagSQLRepository(session=self.uow.session)
