from typing import Any, Generic, TypeVar

from cleanstack.entities import DomainModel
from cleanstack.factories.base import BaseFactory
from tests.factories.entities import (
    DBEntity,
    Post,
    PostEntityFactory,
    User,
    UserEntityFactory,
)

T = TypeVar("T", bound=DomainModel)


class InMemoryBaseFactory(BaseFactory[T], Generic[T]):
    def __init__(self, collection: list[DBEntity]) -> None:
        self.collection = collection

    def _insert_one(self, entity: T) -> None:
        db_entity = self._to_database_entity(entity)
        self.collection.append(db_entity)

    @staticmethod
    def _to_database_entity(entity: T, /) -> DBEntity:
        return entity.model_dump()


class PostFactory(InMemoryBaseFactory[Post]):
    def __init__(self, collection: list[DBEntity]):
        super().__init__(collection=collection)

    @property
    def user_factory(self) -> "UserFactory":
        return UserFactory(collection=self.collection)

    def _build_entity(self, **kwargs: Any) -> Post:
        if "author_id" not in kwargs:
            kwargs["author_id"] = self.user_factory.create_one().id
        return PostEntityFactory.build(**kwargs)


class UserFactory(InMemoryBaseFactory[User]):
    def __init__(self, collection: list[DBEntity]):
        super().__init__(collection=collection)

    def _build_entity(self, **kwargs: Any) -> User:
        return UserEntityFactory.build(**kwargs)
