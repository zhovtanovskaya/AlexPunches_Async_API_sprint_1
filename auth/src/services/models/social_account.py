"""Пидантик модели SocialAccount для сервисов."""
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class SocialAccountBaseModel(BaseModel):
    """Базовая модель SocialAccount."""

    id: UUID | None = None
    user_id: UUID | None = None
    social_id: str
    social_name: Literal['google_oauth'] = 'google_oauth'

    class Config:  # noqa
        orm_mode = True


class SocialAccountCreateModel(BaseModel):
    """Модель для создания SocialAccount."""

    social_id: str
    social_name: Literal['google_oauth'] = 'google_oauth'
