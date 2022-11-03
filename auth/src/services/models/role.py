"""Объектное представление ролей уровня сервисов."""

from pydantic import BaseModel, constr


class Role(BaseModel):
    """Роли, с которыми работают методы RoleService."""

    id: int | None = None
    name: constr(max_length=80) | None = None
    description: constr(max_length=80) | None = None

    class Config:
        orm_mode = True
