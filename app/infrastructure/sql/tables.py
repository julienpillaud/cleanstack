import datetime
import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.items.entities import ItemStatus
from cleanstack.infrastructure.sql.entities import OrmEntity

item_tag_association = Table(
    "item_tag",
    OrmEntity.metadata,
    Column[uuid.UUID](
        "item_id",
        ForeignKey("item.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column[uuid.UUID](
        "tag_id",
        ForeignKey("tag.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class OrmItem(OrmEntity):
    __tablename__ = "item"

    uuid_field: Mapped[uuid.UUID]
    string_field: Mapped[str]
    int_field: Mapped[int]
    float_field: Mapped[float]
    bool_field: Mapped[bool]
    datetime_field: Mapped[datetime.datetime]
    strenum_field: Mapped[ItemStatus]
    optional_field: Mapped[str | None]

    tags: Mapped[list[OrmTag]] = relationship(secondary=item_tag_association)


class OrmTag(OrmEntity):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(unique=True)
