"""Роли уровня сервисов."""

from pydantic import BaseModel, constr


class Role(BaseModel):
    """Роль для сервиса RoleService."""

    id: int | None = None
    name: constr(max_length=80) | None = None
    description: constr(max_length=80) | None = None

    class Config:
        orm_mode = True