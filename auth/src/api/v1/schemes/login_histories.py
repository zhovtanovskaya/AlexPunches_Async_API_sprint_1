"""Схемы истории для API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginHistoryScheme(BaseModel):
    """Основная схема истории."""

    id: UUID
    email: EmailStr
    date_login: datetime

    class Config:  # noqa
        orm_mode = True


class ListLoginHistoryScheme(BaseModel):
    """Список историй логинов пользователей."""

    login_histories: list[LoginHistoryScheme] = []
