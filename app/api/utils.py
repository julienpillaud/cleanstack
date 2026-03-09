from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginatedResponseDTO[T: BaseModel](BaseModel):
    page: PositiveInt
    size: PositiveInt
    pages: NonNegativeInt
    total: NonNegativeInt
    items: list[T]
