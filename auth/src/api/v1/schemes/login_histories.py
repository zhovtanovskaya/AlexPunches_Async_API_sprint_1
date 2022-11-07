"""Схемы истории для API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginHistoryBaseScheme(BaseModel):
    """Базовая схема истории."""

    username: str
    email: EmailStr
    data_create: datetime
    data_login: datetime


class LoginHistoryScheme(LoginHistoryBaseScheme):
    """Основная схема истории."""

    email: EmailStr

    id: UUID


class ListLoginHistoryScheme(BaseModel):
    """Список историй логинов пользователей."""

    login_histories: list[LoginHistoryScheme] = []


class LoginHistoryCreateScheme(LoginHistoryBaseScheme):
    """Использовать при создании истории."""

    username: str
    email: EmailStr
    data_create: datetime
    data_login: datetime