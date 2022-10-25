from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    login: str
    email: EmailStr
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str
    roles: list[str] = []
