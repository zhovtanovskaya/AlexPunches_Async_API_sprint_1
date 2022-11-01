from uuid import UUID

from pydantic import BaseModel, EmailStr

from api.v1.schemes.user_roles import RoleScheme


class UserScheme(BaseModel):
    """Схема пользователя для API."""

    login: str | None = None
    email: EmailStr
    id: UUID
    roles: list[RoleScheme] = []

    class Config:  # noqa
        orm_mode = True
