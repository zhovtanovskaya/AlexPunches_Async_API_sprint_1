from pydantic import BaseModel, Field
from pydantic.types import NonNegativeFloat, NonNegativeInt, PositiveInt

from src.services.ugc.models.base import ContentType, MovieReaction


class Rating(MovieReaction):
    type: ContentType = ContentType.RATING
    value: PositiveInt = Field(gte=0, lte=10)


class RatingStats(BaseModel):
    total_ratings: NonNegativeInt = 0
    average_rating: NonNegativeFloat = 0
