"""Схемы Ролей для API."""
from pydantic import BaseModel, Field


class RoleBaseScheme(BaseModel):
    """Базовая схема Роли.

    В ней все поля необязательные.
    От нее наследуются все остальные, поэтому она используется
    в трансформерах api.v1.schemes.transform_schemes.

    Дочерние модели переопределяют поля как им нужно.
    """

    id: int | None
    name: str = Field(None, max_length=80)
    description: str = Field(None, max_length=80)


class RoleScheme(RoleBaseScheme):
    """Основная схема Роли."""

    id: int
    name: str = Field(..., max_length=80)

    class Config:  # noqa
        orm_mode = True


class RoleCreateScheme(RoleBaseScheme):
    """Схема для создания Роли."""

    name: str = Field(..., max_length=80)


class RoleEditScheme(RoleBaseScheme):
    """Схема редактирования Роли."""

    id: int


class ListRolesScheme(BaseModel):
    """Список схем Ролей."""

    list_roles: list[RoleScheme]
