"""Объектное представление ролей уровня сервисов."""
from pydantic import BaseModel, Field


class RoleBaseModel(BaseModel):
    """Базовая модель Роли.

    В ней все поля необязательные.
    От нее наследуются все остальные, поэтому они используется
        в трансформерах api.v1.schemes.transform_schemes.
    Дочерние модели переопределяют поля как им нужно.
    """

    id: int | None = None
    name: str = Field(None, max_length=80)
    description: str = Field(None, max_length=80)


class RoleModel(RoleBaseModel):
    """Основная модель Роли."""

    id: int
    name: str = Field(..., max_length=80)

    class Config:
        orm_mode = True


class RoleCreateModel(RoleBaseModel):
    """Модель для создания Роли."""

    name: str = Field(..., max_length=80)


class RoleEditModel(RoleBaseModel):
    """Модель редактирования Роли."""

    id: int
