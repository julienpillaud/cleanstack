from typing import Any

from protest import factory

from app.domain.items.entities import Item
from tests.factories.items import generate_item


@factory()
def get_item(**kwargs: Any) -> Item:
    return generate_item(**kwargs)
