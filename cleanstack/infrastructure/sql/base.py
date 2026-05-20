from typing import Any

from sqlalchemy.sql.base import ExecutableOption

from cleanstack.entities import DomainEntity
from cleanstack.infrastructure.sql.entities import OrmEntity


class SQLRepositoryError(Exception):
    pass


class SQLMixin[T: DomainEntity, OrmT: OrmEntity]:
    domain_entity_type: type[T]
    orm_model_type: type[OrmT]
    searchable_fields: tuple[str, ...] = ()

    def to_domain_entity(self, orm_entity: OrmT, /) -> T:
        return self.domain_entity_type.model_validate(orm_entity)

    @property
    def load_options(self) -> list[ExecutableOption]:
        return []

    @staticmethod
    def extra_excluded_fields() -> set[str]:
        return set()

    def _to_database_values(
        self,
        entity: T,
        /,
        exclude: set[str] | None = None,
    ) -> dict[str, Any]:
        exclude = (exclude or set()) | self.extra_excluded_fields()
        return entity.model_dump(exclude=exclude)
