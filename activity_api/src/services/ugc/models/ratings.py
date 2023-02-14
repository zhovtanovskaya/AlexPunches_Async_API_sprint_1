from pydantic import BaseModel, Field
from pydantic.types import NonNegativeFloat, NonNegativeInt

from src.services.ugc.models.base import ContentType, MovieReaction


class Rating(MovieReaction):
    type: ContentType = ContentType.RATING
    value: int = Field(..., ge=0, le=10)


class RatingStats(BaseModel):
    total_ratings: NonNegativeInt = 0
    average_rating: NonNegativeFloat = 0
