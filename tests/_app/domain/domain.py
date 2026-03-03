from cleanstack.domain import BaseDomain, UnitOfWorkProtocol
from cleanstack.domain.handlers import CommandHandler, QueryHandler
from tests._app.domain.context import ContextProtocol
from tests._app.domain.items.commands import (
    failed_command,
    get_items_command,
    successful_command,
    successful_query,
)


class Domain(BaseDomain[UnitOfWorkProtocol, ContextProtocol]):
    get_items = QueryHandler(get_items_command)

    successful_command = CommandHandler(successful_command)
    successful_query = QueryHandler(successful_query)
    failed_command = CommandHandler(failed_command)
