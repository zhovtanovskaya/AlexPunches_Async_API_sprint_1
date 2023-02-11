"""Сущности, общие для всех моделей пользовательского контента."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, Field, validator

from src.services.ugc.models.custom_types import ContentType, StrObjectId


class Reaction(BaseModel):
    """Базовый класс и настройки для пользовательского контента."""

    id: Optional[StrObjectId] = Field(alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    user_id: UUID
    target_type: ContentType
    target_id: StrObjectId

    @classmethod
    @validator('user_id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value

    class Config:
        """Настроить модель для совместимости с Mongo и BSON."""

        # Разрешить в классе поле типа bson.ObjectId.
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MovieReaction(Reaction):
    """Базовый класс для реакций на фильм."""

    target_id: UUID
    target_type: ContentType = ContentType.MOVIE

    @classmethod
    @validator('target_id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value
