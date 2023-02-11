from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.services.ugc.models.custom_types import ContentType, StrObjectId


class _BookmarkBaseScheme(BaseModel):
    id: StrObjectId | None = None
    created_at: datetime | None = None
    user_id: UUID | None = None
    type: ContentType | None = ContentType.BOOKMARK
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE


class BookmarkCreateScheme(_BookmarkBaseScheme):
    pass


class BookmarkScheme(_BookmarkBaseScheme):
    id: str   # TODO как правильно сериализовать StrObjectId в строку?
    created_at: datetime
    user_id: UUID
    type: ContentType = ContentType.BOOKMARK
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE


class BookmarkResultsListScheme(BaseModel):
    results: list[BookmarkScheme] = []
