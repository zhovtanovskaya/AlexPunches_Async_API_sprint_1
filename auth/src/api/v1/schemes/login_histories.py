"""Схемы истории для API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt


class LoginHistoryScheme(BaseModel):
    """Основная схема истории."""

    id: UUID
    email: EmailStr
    date_login: datetime

    class Config:  # noqa
        orm_mode = True


class ListLoginHistoryScheme(BaseModel):
    """Страница историй логинов пользователей."""

    login_histories: list[LoginHistoryScheme] = []
    page_number: PositiveInt
    per_page: PositiveInt
    total_items: PositiveInt
