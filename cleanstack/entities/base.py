import uuid

from pydantic import BaseModel, ConfigDict

type EntityId = uuid.UUID


class DomainEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: EntityId
