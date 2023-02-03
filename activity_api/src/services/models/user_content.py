from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field


class ContentType(str, Enum):
    MOVIE = 'movie'
    REVIEW = 'review'
    BOOKMARK = 'bookmark'
    RATING = 'rating'
    LIKE = 'like'


class LikeValue(int, Enum):
    LIKE = 10
    DISLIKE = 0


class StrObjectId(ObjectId):
    """Класс для приведения строки к типу ObjecId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId.")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Like(BaseModel):
    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    user_id: UUID
    type: ContentType = ContentType.LIKE
    target_id: StrObjectId
    target_type: ContentType = ContentType.REVIEW
    value: LikeValue

    class Config:
        # Разрешить в классе поле типа bson.ObjectId.
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
