from unittest.mock import MagicMock

import pytest

from tests.init.context import Context, ContextProtocol
from tests.init.domain import Domain
from tests.init.uow import (
    Settings,
)


@pytest.fixture
def context() -> ContextProtocol:
    mock_sql_uow = MagicMock()
    mock_mongo_uow = MagicMock()

    real_context = Context(settings=Settings())

    real_context.sql_uow = mock_sql_uow
    real_context.mongo_uow = mock_mongo_uow
    real_context.members = [mock_sql_uow, mock_mongo_uow]

    return real_context


@pytest.fixture
def domain(context: ContextProtocol) -> Domain:
    return Domain(context=context)
