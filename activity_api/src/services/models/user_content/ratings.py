from pydantic import BaseModel, Field
from pydantic.types import NonNegativeInt, PositiveFloat, PositiveInt

from .base import ContentType, MovieReaction


class Rating(MovieReaction):
    type: ContentType = ContentType.RATING
    value: PositiveInt = Field(gte=0, lte=10)


class RatingStats(BaseModel):
    total_ratings: NonNegativeInt
    average_rating: PositiveFloat
