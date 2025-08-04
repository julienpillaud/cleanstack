from typing import Any, ClassVar, TypeAlias

from polyfactory.factories.pydantic_factory import ModelFactory

from cleanstack.entities import DomainModel, EntityId

DBEntity: TypeAlias = dict[str, Any]


class Post(DomainModel):
    content: str
    author_id: EntityId


class User(DomainModel):
    name: str
    posts: list[Post]


class PostEntityFactory(ModelFactory[Post]): ...


class UserEntityFactory(ModelFactory[User]):
    # create user without posts to avoid circular dependency
    posts: ClassVar[list[Post]] = []
