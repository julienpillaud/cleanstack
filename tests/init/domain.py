from cleanstack.domain import BaseDomain
from cleanstack.handlers import CommandHandler, QueryHandler
from cleanstack.uow import UnitOfWorkProtocol
from tests.init.context import ContextProtocol


def successful_command(context: ContextProtocol, x: str) -> str:
    context.user_adapter.get()
    return f"command executed with {x}"


def successful_query(context: ContextProtocol, x: str) -> str:
    return f"query executed with {x}"


def failed_command(context: ContextProtocol) -> str:
    raise ValueError("command failed")


class Domain(BaseDomain[UnitOfWorkProtocol, ContextProtocol]):
    successful_command = CommandHandler(successful_command)
    successful_query = QueryHandler(successful_query)
    failed_command = CommandHandler(failed_command)
