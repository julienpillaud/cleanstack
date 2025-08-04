import uuid

from tests.factories.entities import DBEntity, PostEntityFactory, UserEntityFactory
from tests.factories.factories import PostFactory, UserFactory


def test_create_user_entity() -> None:
    user = UserEntityFactory.build()
    assert isinstance(user.id, uuid.UUID)
    assert isinstance(user.name, str)
    assert user.posts == []


def test_create_post_entity() -> None:
    user = UserEntityFactory.build()
    post = PostEntityFactory.build(author_id=user.id)

    assert isinstance(post.id, uuid.UUID)
    assert isinstance(post.content, str)
    assert post.author_id == user.id


def test_create_user(user_factory: UserFactory, collection: list[DBEntity]) -> None:
    user_id = uuid.uuid4()
    user = user_factory.create_one(id=user_id, name="Test User")

    assert user.id == user_id
    assert user.name == "Test User"
    assert user.posts == []

    assert collection
    user_db = collection[0]
    assert user_db["id"] == user_id
    assert user_db["name"] == "Test User"
    assert user_db["posts"] == []


def test_create_post(
    user_factory: UserFactory,
    post_factory: PostFactory,
    collection: list[DBEntity],
) -> None:
    post_id = uuid.uuid4()
    user = user_factory.create_one()
    post = post_factory.create_one(
        id=post_id,
        content="Test Post",
        author_id=user.id,
    )

    assert post.id == post_id
    assert post.content == "Test Post"
    assert post.author_id == user.id

    assert collection
    post_db = collection[1]
    assert post_db["id"] == post_id
    assert post_db["content"] == "Test Post"
    assert post_db["author_id"] == user.id
