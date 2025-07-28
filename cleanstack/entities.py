import uuid
from typing import TypeAlias

from pydantic import BaseModel, ConfigDict

EntityId: TypeAlias = uuid.UUID


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: EntityId
