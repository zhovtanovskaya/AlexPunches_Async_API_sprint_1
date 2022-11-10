"""Пидантик модели LoginHistory для сервисов."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginHistoryCreateModel(BaseModel):
    """Модель для создания истории логирования пользователя."""

    username: str
    email: EmailStr
    date_login: datetime


class LoginHistoryModel(BaseModel):
    """Модель истории логирования пользователя."""

    id: UUID
