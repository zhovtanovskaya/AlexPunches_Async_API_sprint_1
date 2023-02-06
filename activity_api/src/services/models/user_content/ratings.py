from pydantic import Field
from pydantic.types import PositiveInt

from .base import ContentType, MovieReaction


class Rating(MovieReaction):
    type: ContentType = ContentType.RATING
    value: PositiveInt = Field(gte=0, lte=10)
