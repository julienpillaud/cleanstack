from app.domain.context import ContextProtocol
from app.domain.items.commands import get_item_command, get_items_command
from cleanstack.domain import BaseDomain, UnitOfWorkProtocol
from cleanstack.domain.handlers import QueryHandler


class Domain(BaseDomain[UnitOfWorkProtocol, ContextProtocol]):
    get_items = QueryHandler(get_items_command)
    get_item = QueryHandler(get_item_command)
