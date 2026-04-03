import random
import uuid
from typing import Any

from protest import factory

from app.domain.items.entities import Item, ItemStatus
from protests.factories.utils import gen_datetime, optional_choice


@factory()
def item(**kwargs: Any) -> Item:
    return Item(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        uuid_field=kwargs["uuid_field"] if "uuid_field" in kwargs else uuid.uuid7(),
        string_field=kwargs.get("string_field", "Test"),
        int_field=kwargs.get("int_field", 42),
        float_field=kwargs.get("float_field", 3.14),
        bool_field=kwargs.get("bool_field", True),
        datetime_field=kwargs["datetime_field"]
        if "datetime_field" in kwargs
        else gen_datetime(),
        strenum_field=kwargs["strenum_field"]
        if "strenum_field" in kwargs
        else random.choice(list(ItemStatus)),
        optional_field=kwargs["optional_field"]
        if "optional_field" in kwargs
        else optional_choice(list(ItemStatus)),
        tags=kwargs.get("tags", []),
    )
