from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator

from src.services.ugc.models.custom_types import ContentType, StrObjectId


class BookmarkBaseScheme(BaseModel):
    id: StrObjectId | None = None
    created_at: datetime | None = None
    user_id: UUID | None = None
    type: ContentType | None = ContentType.BOOKMARK
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE


class BookmarkCreateScheme(BookmarkBaseScheme):
    created_at: datetime | None = Field(default_factory=datetime.now)


class BookmarkScheme(BookmarkBaseScheme):
    id: StrObjectId   # TODO как правильно сериализовать StrObjectId в строку?
    created_at: datetime
    user_id: UUID
    type: ContentType = ContentType.BOOKMARK
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE

    @validator('id')
    def validate_objectid(cls, value):
        if value:
            return str(value)
        return value


class BookmarkResultsListScheme(BaseModel):
    results: list[BookmarkScheme] = []
