import datetime
import random
from collections.abc import Sequence


def gen_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def optional_choice[T](iterable: Sequence[T]) -> T | None:
    optional = random.choice([True, False])
    return random.choice(iterable) if optional else None
