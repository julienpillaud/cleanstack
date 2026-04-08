from app.domain.containers.commands import (
    create_container_command,
    delete_container_command,
    get_container_command,
    update_container_command,
)
from app.domain.context import ContextProtocol
from app.domain.items.commands import (
    create_item_command,
    delete_item_command,
    get_item_command,
    get_items_command,
    update_item_command,
)
from cleanstack.domain import BaseDomain, UnitOfWorkProtocol
from cleanstack.domain.handlers import CommandHandler, QueryHandler


class Domain(BaseDomain[UnitOfWorkProtocol, ContextProtocol]):
    get_items = QueryHandler(get_items_command)
    get_item = QueryHandler(get_item_command)
    create_item = CommandHandler(create_item_command)
    update_item = CommandHandler(update_item_command)
    delete_item = CommandHandler(delete_item_command)

    get_container = QueryHandler(get_container_command)
    create_container = CommandHandler(create_container_command)
    update_container = CommandHandler(update_container_command)
    delete_container = CommandHandler(delete_container_command)
