from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    """Модель данных юзера."""

    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class PostingBaseModel(BaseModel):
    """Базовая модель отправления."""

    deadline: datetime
    user: UserInfo

    def json_bytes(self):
        """Получить JSON объекта в виде байт-строки."""
        return self.json().encode()


class WelcomeEmailPosting(PostingBaseModel):
    """Модель отправления приветственного письма."""

    pass
