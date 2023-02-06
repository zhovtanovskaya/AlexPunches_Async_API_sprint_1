from enum import Enum

from .base import ContentType, Reaction, StrObjectId


class LikeValue(int, Enum):
    """Возможные эмоции в лайке."""

    LIKE = 10
    DISLIKE = 0


class Like(Reaction):
    """Объектное представление лайка или дизлайка рецензии из Mongo."""

    type: ContentType = ContentType.LIKE
    target_id: StrObjectId
    target_type: ContentType = ContentType.REVIEW
    value: LikeValue
