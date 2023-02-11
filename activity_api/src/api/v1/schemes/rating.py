from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator

from src.services.ugc.models.custom_types import ContentType, StrObjectId


class RatingBaseScheme(BaseModel):
    id: StrObjectId | None = None
    created_at: datetime | None = None
    user_id: UUID | None = None
    type: ContentType | None = ContentType.LIKE
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE
    value: int = Field(..., ge=0, le=10)


class RatingCreateScheme(RatingBaseScheme):
    created_at: datetime | None = Field(default_factory=datetime.now)


class RatingScheme(RatingBaseScheme):
    id: StrObjectId
    created_at: datetime
    user_id: UUID
    type: ContentType = ContentType.LIKE
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE

    @validator('id')
    def validate_objectid(cls, value):
        if value:
            return str(value)
        return value
