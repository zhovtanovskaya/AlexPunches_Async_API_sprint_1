"""Схемы Роли для API."""

from pydantic import BaseModel


class RoleScheme(BaseModel):
    """Роль."""

    id: int
    name: str
    description: str | None = None

    class Config:  # noqa
        orm_mode = True


class UserRoleCreateScheme(BaseModel):
    """Использовать при добавлении Юзер-Роли."""

    name: str


class ListUserRolesScheme(BaseModel):
    """Список Ролей."""

    user_roles: list[RoleScheme] = []
