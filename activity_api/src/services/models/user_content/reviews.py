from enum import Enum

from .base import ContentType, MovieReaction


class ReviewValue(int, Enum):
    """Отношение рецензента к фильму."""

    POSITIVE = 10
    NEUTRAL = 5
    NEGATIVE = 0


class Review(MovieReaction):
    """Рецензия на фильм.

    Состоит из заголовка, текста и отношения к фильму, которое
    рецензент высказывает в рецензии.  Например, если рецензия
    одобряет фильм, то отношение положительное ("positive")
    """

    type: ContentType = ContentType.REVIEW
    value: ReviewValue
    title: str
    text: str
