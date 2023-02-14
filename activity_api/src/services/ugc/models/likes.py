from enum import Enum

from src.services.ugc.models.base import ContentType, Reaction
from src.services.ugc.models.custom_types import StrObjectId


class LikeValue(int, Enum):
    """Возможные эмоции в лайке."""

    LIKE = 10
    DISLIKE = 0


class Like(Reaction):
    """Объектное представление лайка или дизлайка рецензии из Mongo."""

    target_id: StrObjectId
    type: ContentType = ContentType.LIKE
    target_type: ContentType = ContentType.REVIEW
    value: LikeValue
