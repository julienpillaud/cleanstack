from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import Mock

import pytest

from cleanstack.domain import BaseDomain, CommandHandler, ContextProtocol


def successful_command(context: ContextProtocol, x: str) -> str:
    return f"command executed with {x}"


def failed_command(context: ContextProtocol) -> str:
    raise ValueError("command failed")


class MockContext(ContextProtocol):
    transaction: Mock
    commit: Mock
    rollback: Mock


class DomainTest(BaseDomain):
    successful_command = CommandHandler(successful_command)
    failed_command = CommandHandler(failed_command)


@pytest.fixture
def context() -> MockContext:
    mock_context = Mock(spec=ContextProtocol)

    @contextmanager
    def mock_transaction() -> Iterator[None]:
        yield

    mock_context.transaction = mock_transaction
    return mock_context


@pytest.fixture
def domain(context: ContextProtocol) -> DomainTest:
    return DomainTest(context=context)
