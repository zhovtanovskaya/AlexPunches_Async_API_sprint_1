from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field

from .base import ContentType, StrObjectId


class LikeValue(int, Enum):
    """Возможные эмоции в лайке."""

    LIKE = 10
    DISLIKE = 0


class Like(BaseModel):
    """Объектное представление лайка из Mongo."""

    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    user_id: UUID
    type: ContentType = ContentType.LIKE
    target_id: StrObjectId
    target_type: ContentType = ContentType.REVIEW
    value: LikeValue

    class Config:
        """Настроить модель для совместимости с Mongo и BSON."""

        # Разрешить в классе поле типа bson.ObjectId.
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
