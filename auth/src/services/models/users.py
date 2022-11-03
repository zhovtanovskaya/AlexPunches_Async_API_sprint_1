"""Пидантик модели User для сервисов."""

from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    """Модель для создания пользователя."""

    email: EmailStr
    password: str


class UserEditModel(BaseModel):
    """Модель редактирования пользователя."""

    email: EmailStr | None = None
    login: str | None = None
    password: str | None = None
