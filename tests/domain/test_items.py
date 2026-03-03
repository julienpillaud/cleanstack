import pytest

from tests._app.domain.domain import Domain


def test_get_items(domain: Domain) -> None:
    assert domain.get_items() == []


def test_successful_command(domain: Domain) -> None:
    result = domain.successful_command(x="test input")
    assert result == "command executed with test input"


def test_successful_query(domain: Domain) -> None:
    result = domain.successful_query(x="test input")
    assert result == "query executed with test input"


def test_failed_command(domain: Domain) -> None:
    with pytest.raises(ValueError, match="command failed"):
        domain.failed_command()
