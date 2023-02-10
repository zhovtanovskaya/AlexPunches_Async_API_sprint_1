from enum import Enum

from src.services.ugc.models.base import ContentType, Reaction


class LikeValue(int, Enum):
    """Возможные эмоции в лайке."""

    LIKE = 10
    DISLIKE = 0


class Like(Reaction):
    """Объектное представление лайка или дизлайка рецензии из Mongo."""

    type: ContentType = ContentType.LIKE
    target_type: ContentType = ContentType.REVIEW
    value: LikeValue
