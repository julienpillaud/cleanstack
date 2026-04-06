from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginatedResponseDTO[T: BaseModel](BaseModel):
    page: PositiveInt
    size: PositiveInt
    pages: NonNegativeInt
    total: NonNegativeInt
    items: list[T]


def get_search(search: str | None = None) -> str | None:
    return search
