"""Схемы пользователя для API."""

from uuid import UUID

from pydantic import BaseModel, EmailStr

from api.v1.schemes.user_roles import RoleScheme


class UserBaseScheme(BaseModel):
    """Базовая схема пользователя."""

    email: EmailStr | None = None
    login: str | None = None


class UserScheme(UserBaseScheme):
    """Основная схема пользователя."""

    email: EmailStr

    id: UUID
    roles: list[RoleScheme] = []


class UserCreateScheme(UserBaseScheme):
    """Использовать при создании пользователя и регистрации."""

    email: EmailStr
    password: str


class UserEditScheme(UserBaseScheme):
    """Использовать для редактирования пользователя."""

    password: str | None = None
