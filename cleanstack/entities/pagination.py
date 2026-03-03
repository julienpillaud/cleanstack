import math

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from cleanstack.entities.base import DomainEntity

DEFAULT_PAGINATION_SIZE = 100


class Pagination(BaseModel):
    page: PositiveInt = 1
    size: PositiveInt = DEFAULT_PAGINATION_SIZE

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size

    def pages(self, total: NonNegativeInt) -> NonNegativeInt:
        return math.ceil(total / self.size)


class PaginatedResponse[T: DomainEntity](BaseModel):
    page: PositiveInt
    size: PositiveInt
    pages: NonNegativeInt
    total: NonNegativeInt
    items: list[T]
