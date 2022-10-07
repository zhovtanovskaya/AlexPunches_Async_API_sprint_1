from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    login: str
    email: EmailStr
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    login: str | None
    email: EmailStr | None


class UserScheme(UserBase):
    id: UUID

    class Config:
        orm_mode = True
