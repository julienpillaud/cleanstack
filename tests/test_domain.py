import pytest

from tests.conftest import DomainTest, MockContext


def test_successful_command(domain: DomainTest, context: MockContext) -> None:
    result = domain.successful_command(x="test input")

    assert result == "command executed with test input"
    context.commit.assert_called_once()
    context.rollback.assert_not_called()


def test_failed_command(domain: DomainTest, context: MockContext) -> None:
    with pytest.raises(ValueError, match="command failed"):
        domain.failed_command()

    context.commit.assert_not_called()
    context.rollback.assert_called_once()
