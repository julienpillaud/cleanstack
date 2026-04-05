import datetime
import random
import string
from collections.abc import Sequence


class Faker:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)

    def random_bool(self) -> bool:
        return self.random.choice([True, False])

    def random_int(self, min_value: int = 0, max_value: int = 100) -> int:
        return self.random.randint(min_value, max_value)

    def random_float(self, min_value: int = 0, max_value: int = 100) -> float:
        return self.random.uniform(min_value, max_value)

    def random_string(self, string_length: int = 10) -> str:
        return "".join(self.random.choices(string.ascii_letters, k=string_length))

    def random_datetime(self) -> datetime.datetime:
        current_datetime = datetime.datetime.now(datetime.UTC)
        return datetime.datetime(
            year=self.random_int(1900, current_datetime.year),
            month=self.random_int(1, 12),
            day=self.random_int(1, 28),
            hour=self.random_int(0, 23),
            minute=self.random_int(0, 59),
            second=self.random_int(0, 59),
        )

    def choice[T](self, iterable: Sequence[T]) -> T:
        return self.random.choice(iterable)

    def optional_choice[T](self, iterable: Sequence[T]) -> T | None:
        optional = self.random.choice([True, False])
        return self.random.choice(iterable) if optional else None


faker = Faker(42)
