"""Схемы пользователя для API."""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

import api.v1.schemes.roles as role_schemes


class UserBaseScheme(BaseModel):
    """Базовая схема пользователя.

    В ней все поля необязательные.
    От нее наследуются !почти все остальные, поэтому она используется
    в трансформерах api.v1.schemes.transform_schemes.

    Дочерние схемы переопределяют поля как им нужно.
    """

    id: UUID | None = None
    email: EmailStr | None = None
    login: str | None = None
    password: str | None = None
    roles: list[role_schemes.RoleScheme] = []
    active: bool | None = None


class UserScheme(BaseModel):
    """Основная схема пользователя.

    !Не наследуется от UserBaseScheme, т.к. не должна содержать "password"!
    """

    id: UUID
    email: EmailStr
    active: bool
    login: str | None = None
    roles: list[role_schemes.RoleScheme] = []

    class Config:  # noqa
        orm_mode = True


class UserCreateScheme(UserBaseScheme):
    """Использовать при создании пользователя и регистрации."""

    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:  # noqa
        anystr_strip_whitespace = True


class UserEditScheme(UserBaseScheme):
    """Использовать для редактирования пользователя."""

    password: str | None = None
