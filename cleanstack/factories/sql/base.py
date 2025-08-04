from typing import Generic, TypeVar

try:
    from sqlalchemy.orm import Session
except ImportError as e:
    raise RuntimeError(
        'To use SQLAlchemy utilities, you need to install "cleanstack[sql]"'
    ) from e

from cleanstack.entities import DomainModel
from cleanstack.factories.base import BaseFactory
from cleanstack.infrastructure.sql.entities import OrmBase

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P", bound=OrmBase)


class SqlBaseFactory(BaseFactory[T], Generic[T, P]):
    orm_model: type[P]

    def __init__(self, session: Session):
        self.session = session

    def _insert_one(self, entity: T) -> None:
        db_entity = self._to_database_entity(entity)
        self.session.add(db_entity)
        self.session.commit()

    def _to_database_entity(self, entity: T) -> P:
        return self.orm_model(**entity.model_dump())
