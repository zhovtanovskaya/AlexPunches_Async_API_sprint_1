from uuid import UUID

from pydantic import BaseModel, EmailStr
from routers.v1.schemes.roles import RoleScheme


class UserBase(BaseModel):
    login: str
    email: EmailStr
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str
    roles: list[str] = []


class UserEdit(UserBase):
    login: str | None
    email: EmailStr | None
    roles: list[str] = []


class UserScheme(UserBase):
    id: UUID
    roles: list[RoleScheme] = []

    class Config:
        orm_mode = True
