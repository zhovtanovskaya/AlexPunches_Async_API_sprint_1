from pydantic import BaseModel, NonNegativeInt, PositiveInt


class Paginator(BaseModel):
    total_pages: NonNegativeInt
    total_items: NonNegativeInt
    number: PositiveInt
    size: PositiveInt
