from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator

from src.api.v1.schemes.paginator import Paginator
from src.services.ugc.models.custom_types import ContentType, StrObjectId


class ReviewBaseScheme(BaseModel):
    created_at: datetime | None = None
    user_id: UUID | None = None
    type: ContentType | None = ContentType.REVIEW
    target_id: UUID
    target_type: ContentType = ContentType.MOVIE
    value: int = Field(5, ge=0, le=10, multiple_of=5)
    title: str = Field(
        ..., min_length=2, max_length=140, strip_whitespace=True,
    )
    text: str = Field(
        ..., min_length=100, max_length=5000, strip_whitespace=True,
    )


class ReviewCreateScheme(ReviewBaseScheme):
    created_at: datetime | None = Field(default_factory=datetime.now)


class ReviewScheme(ReviewBaseScheme):
    id: StrObjectId
    created_at: datetime
    user_id: UUID
    type: ContentType = ContentType.REVIEW

    @validator('id')
    def validate_objectid(cls, value):
        if value:
            return str(value)
        return value


class ReviewPaginateScheme(BaseModel):
    page: Paginator
    results: list[ReviewScheme] = []
