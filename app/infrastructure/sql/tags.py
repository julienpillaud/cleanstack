from app.domain.tags.entities import Tag
from app.domain.tags.repository import TagRepositoryProtocol
from app.infrastructure.sql.tables import OrmTag
from cleanstack.infrastructure.sql.base import SQLRepository


class TagSQLRepository(SQLRepository[Tag, OrmTag], TagRepositoryProtocol):
    domain_entity_type = Tag
    orm_model_type = OrmTag
