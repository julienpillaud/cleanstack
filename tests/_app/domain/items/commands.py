from typing import Any

from tests._app.domain.context import ContextProtocol


def get_items_command(context: ContextProtocol) -> Any:
    return context.item_repository.get()


def successful_command(context: ContextProtocol, x: str) -> str:
    return f"command executed with {x}"


def successful_query(context: ContextProtocol, x: str) -> str:
    return f"query executed with {x}"


def failed_command(context: ContextProtocol) -> str:
    raise ValueError("command failed")
