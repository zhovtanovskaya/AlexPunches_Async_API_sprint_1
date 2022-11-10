from pydantic import BaseModel, EmailStr


class UserSigninScheme(BaseModel):
    """Использовать при создании пользователя и регистрации."""

    email: EmailStr
    password: str

    class Config:
        """Общие для логина и пароля настройки."""

        anystr_strip_whitespace = True
        min_anystr_length = 1
