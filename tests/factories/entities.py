from typing import Any, ClassVar

from polyfactory.factories.pydantic_factory import ModelFactory

from cleanstack.entities import DomainModel, EntityId

type DBEntity = dict[str, Any]


class Post(DomainModel):
    content: str
    author_id: EntityId


class User(DomainModel):
    name: str
    posts: list[Post]


class PostEntityFactory(ModelFactory[Post]):
    __check_model__ = True


class UserEntityFactory(ModelFactory[User]):
    __check_model__ = True
    # create user without posts to avoid circular dependency
    posts: ClassVar[list[Post]] = []
