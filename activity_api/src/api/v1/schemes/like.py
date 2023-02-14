from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator

from src.services.ugc.models.custom_types import ContentType, StrObjectId


class LikeBaseScheme(BaseModel):
    created_at: datetime | None = None
    user_id: UUID | None = None
    type: ContentType | None = ContentType.LIKE
    target_id: StrObjectId
    target_type: ContentType = ContentType.REVIEW
    value: int = Field(..., ge=0, le=10, multiple_of=10)


class LikeCreateScheme(LikeBaseScheme):
    created_at: datetime | None = Field(default_factory=datetime.now)


class LikeScheme(LikeBaseScheme):
    id: StrObjectId
    created_at: datetime
    user_id: UUID
    type: ContentType = ContentType.LIKE

    @validator('id', 'target_id')
    def validate_objectid(cls, value):
        if value:
            return str(value)
        return value
