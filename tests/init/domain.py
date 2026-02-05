from cleanstack.domain import BaseDomain, CommandHandler
from tests.init.context import ContextProtocol


def successful_command(context: ContextProtocol, x: str) -> str:
    context.user_adapter.get()
    return f"command executed with {x}"


def failed_command(context: ContextProtocol) -> str:
    raise ValueError("command failed")


class Domain(BaseDomain[ContextProtocol]):
    successful_command = CommandHandler(successful_command)
    failed_command = CommandHandler(failed_command)
