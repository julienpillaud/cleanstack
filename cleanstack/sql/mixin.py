from sqlalchemy.sql.base import ExecutableOption

from cleanstack.entities import BaseEntity
from cleanstack.sql.entities import OrmEntity


class SQLMixin[T: BaseEntity, OrmT: OrmEntity]:
    domain_entity_type: type[T]
    orm_model_type: type[OrmT]
    searchable_fields: tuple[str, ...] = ()

    def to_orm_entity(self, entity: T) -> OrmEntity:
        return self.orm_model_type(**entity.model_dump())

    def to_domain_entity(self, orm_entity: OrmT, /) -> T:
        return self.domain_entity_type.model_validate(orm_entity)

    @property
    def load_options(self) -> list[ExecutableOption]:
        return []
