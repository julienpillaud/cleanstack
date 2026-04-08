import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.items.entities import ItemStatus
from cleanstack.infrastructure.sql.entities import OrmEntity


class OrmItem(OrmEntity):
    __tablename__ = "item"

    uuid_field: Mapped[uuid.UUID]
    string_field: Mapped[str]
    int_field: Mapped[int]
    float_field: Mapped[float]
    bool_field: Mapped[bool]
    datetime_field: Mapped[datetime.datetime]
    strenum_field: Mapped[ItemStatus]
    optional_field: Mapped[ItemStatus | None]
    computed_field: Mapped[float]


class OrmNode(OrmEntity):
    __tablename__ = "node"

    label: Mapped[str]
    container_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("container.id"))


class OrmContainer(OrmEntity):
    __tablename__ = "container"

    name: Mapped[str]
    nodes: Mapped[list[OrmNode]] = relationship()
