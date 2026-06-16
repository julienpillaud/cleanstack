from typing import Any

from sqlalchemy import Column, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from cleanstack.entities import EntityId


class OrmEntity(DeclarativeBase):
    id: Mapped[EntityId] = mapped_column(primary_key=True)

    @classmethod
    def columns_map(cls) -> dict[str, Column[Any]]:
        mapper = inspect(cls)
        return {column.name: column for column in mapper.columns}
