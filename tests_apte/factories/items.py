from typing import Any

from apte import factory

from app.domain.items.entities import Item
from tests.factories.items import generate_item


@factory()
def get_item(**kwargs: Any) -> Item:  # noqa: ANN401
    return generate_item(**kwargs)
