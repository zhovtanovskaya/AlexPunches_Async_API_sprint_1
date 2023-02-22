from datetime import datetime

from pydantic import BaseModel, EmailStr

from core.config import config


class UserInfoModel(BaseModel):
    """Модель данных юзера."""

    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    timezone: str = config.def_timezone


class PostingBaseModel(BaseModel):
    """Базовая модель отправления."""

    deadline: datetime
    user: UserInfoModel


class WelcomeEmailPosting(PostingBaseModel):
    """Модель отправления приветственного письма."""

    pass
