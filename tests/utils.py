import datetime
import uuid


def assert_uuid(actual: str, expected: uuid.UUID) -> None:
    assert uuid.UUID(actual) == expected


def assert_datetime(actual: str, expected: datetime.datetime) -> None:
    assert datetime.datetime.fromisoformat(actual) == expected
