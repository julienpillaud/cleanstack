import uuid

try:
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
except ImportError as e:
    raise RuntimeError(
        'To use SQLAlchemy utilities, you need to install "cleanstack[sql]"'
    ) from e


class OrmBase(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
