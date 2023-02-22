"""Пидантик модели User для сервисов."""
from uuid import UUID

from pydantic import BaseModel, EmailStr

import services.models.roles as service_role_models


class UserBaseModel(BaseModel):
    """Базовая модель пользователя."""

    id: UUID | None = None
    email: EmailStr | None = None
    password: str | None = None
    roles: list[service_role_models.RoleModel] = []
    active: bool | None = None
    is_email_confirmed: bool | None = None
    confirmation_code: UUID | None = None


class UserModel(UserBaseModel):
    """Основная модель пользователя."""

    id: UUID
    email: EmailStr
    active: bool
    is_email_confirmed: bool

    class Config:  # noqa
        orm_mode = True


class UserCreateModel(UserBaseModel):
    """Модель для создания пользователя."""

    email: EmailStr
    password: str


class UserEditModel(UserBaseModel):
    """Модель редактирования пользователя."""

    id: UUID
    password: str | None = None
