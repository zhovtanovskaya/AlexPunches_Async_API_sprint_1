"""Сущности, общие для всех моделей пользовательского контента."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field


class StrObjectId(ObjectId):
    """Класс для приведения строки к типу ObjecId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId.')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ContentType(str, Enum):
    """Типы пользовательского контента в Mongo."""

    MOVIE = 'movie'
    REVIEW = 'review'
    BOOKMARK = 'bookmark'
    RATING = 'rating'
    LIKE = 'like'


class Reaction(BaseModel):
    """Базовый класс и настройки для пользовательского контента."""

    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    user_id: UUID
    target_type: ContentType
    target_id: StrObjectId

    class Config:
        """Настроить модель для совместимости с Mongo и BSON."""

        # Разрешить в классе поле типа bson.ObjectId.
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MovieReaction(Reaction):
    """Базовый класс для реакций на фильм."""

    target_id: UUID
    target_type: ContentType = ContentType.MOVIE
