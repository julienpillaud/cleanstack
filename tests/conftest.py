from unittest.mock import MagicMock

import pytest

from cleanstack.domain import CompositeUniOfWork
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from tests._app.core.context import Context
from tests._app.domain.domain import Domain


class ContextTest(Context):
    @property
    def item_repository(self) -> MagicMock:
        mock_repository = MagicMock()
        mock_repository.get.return_value = []
        return mock_repository


@pytest.fixture
def mongo_context() -> MongoContext:
    return MongoContext.from_settings(
        host="test",
        database_name="test",
    )


@pytest.fixture
def mongo_uow(mongo_context: MongoContext) -> MongoUnitOfWork:
    return MongoUnitOfWork(context=mongo_context)


@pytest.fixture
def context(mongo_context: MongoContext, mongo_uow: MongoUnitOfWork) -> ContextTest:
    return ContextTest(mongo_context=mongo_context, mongo_uow=mongo_uow)


@pytest.fixture
def domain(context: ContextTest) -> Domain:
    uow = CompositeUniOfWork(members=context.members)
    return Domain(uow=uow, context=context)
