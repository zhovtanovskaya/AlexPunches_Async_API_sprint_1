"""Пидантик модели LoginHistory для сервисов."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginHistoryCreateModel(BaseModel):
    """Модель для создания истории логирования пользователя."""

    email: EmailStr
    date_login: datetime
    user_agent: str


class LoginHistoryModel(BaseModel):
    """Модель истории логирования пользователя."""

    id: UUID
