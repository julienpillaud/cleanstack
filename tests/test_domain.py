from typing import cast
from unittest.mock import MagicMock

import pytest

from tests.init.context import Context
from tests.init.domain import Domain


def test_successful_command(domain: Domain, context: Context) -> None:
    result = domain.successful_command(x="test input")

    assert result == "command executed with test input"
    cast(MagicMock, context.uow.sql.commit).assert_called_once()
    cast(MagicMock, context.uow.mongo.commit).assert_called_once()
    cast(MagicMock, context.uow.sql.rollback).assert_not_called()
    cast(MagicMock, context.uow.mongo.rollback).assert_not_called()


def test_successful_query(domain: Domain, context: Context) -> None:
    result = domain.successful_query(x="test input")

    assert result == "query executed with test input"
    cast(MagicMock, context.uow.sql.commit).assert_not_called()
    cast(MagicMock, context.uow.mongo.commit).assert_not_called()
    cast(MagicMock, context.uow.sql.rollback).assert_not_called()
    cast(MagicMock, context.uow.mongo.rollback).assert_not_called()


def test_failed_command(domain: Domain, context: Context) -> None:
    with pytest.raises(ValueError, match="command failed"):
        domain.failed_command()

    cast(MagicMock, context.uow.sql.commit).assert_not_called()
    cast(MagicMock, context.uow.mongo.commit).assert_not_called()
    cast(MagicMock, context.uow.sql.rollback).assert_called_once()
    cast(MagicMock, context.uow.mongo.rollback).assert_called_once()
