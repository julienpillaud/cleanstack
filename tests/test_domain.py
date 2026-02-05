from unittest.mock import MagicMock

import pytest

from tests.init.domain import Domain


def test_successful_command(domain: Domain, context: MagicMock) -> None:
    result = domain.successful_command(x="test input")

    assert result == "command executed with test input"
    context.sql_uow.commit.assert_called_once()
    context.mongo_uow.commit.assert_called_once()
    context.sql_uow.rollback.assert_not_called()
    context.mongo_uow.rollback.assert_not_called()


def test_failed_command(domain: Domain, context: MagicMock) -> None:
    with pytest.raises(ValueError, match="command failed"):
        domain.failed_command()

    context.sql_uow.commit.assert_not_called()
    context.mongo_uow.commit.assert_not_called()
    context.sql_uow.rollback.assert_called_once()
    context.mongo_uow.rollback.assert_called_once()
