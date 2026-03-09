import datetime
import uuid

from sqlalchemy.orm import Mapped

from cleanstack.infrastructure.sql.entities import OrmEntity


class OrmItem(OrmEntity):
    __tablename__ = "item"

    uuid_field: Mapped[uuid.UUID]
    string_field: Mapped[str]
    int_field: Mapped[int]
    float_field: Mapped[float]
    bool_field: Mapped[bool]
    datetime_field: Mapped[datetime.datetime]
    optional_field: Mapped[str | None]
