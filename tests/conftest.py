from unittest.mock import MagicMock, Mock

import pytest

from tests.init.context import Context
from tests.init.domain import Domain
from tests.init.uow import (
    MongoUnitOfWork,
    SQLUnitOfWork,
    UnitOfWork,
)


@pytest.fixture
def uow() -> UnitOfWork:
    sql_uow = Mock(
        spec=SQLUnitOfWork,
        session="session",
        transaction=MagicMock(),
    )
    mongo_uow = Mock(
        spec=MongoUnitOfWork,
        client="client",
        transaction=MagicMock(),
    )
    return UnitOfWork(sql=sql_uow, mongo=mongo_uow)


@pytest.fixture
def context(uow: UnitOfWork) -> Context:
    return Context(uow=uow)


@pytest.fixture
def domain(uow: UnitOfWork, context: Context) -> Domain:
    return Domain(uow=uow, context=context)
