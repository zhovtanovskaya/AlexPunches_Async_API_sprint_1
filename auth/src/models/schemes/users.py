from pydantic import BaseModel, EmailStr


class UserBaseScheme(BaseModel):
    """Базовая схема пользователя."""

    login: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserCreateScheme(UserBaseScheme):
    """Использовать при создании пользователя и регистрации."""

    email: EmailStr
    password: str


class UserEditScheme(UserBaseScheme):
    """Использовать для редактирования пользователя."""

    ...
