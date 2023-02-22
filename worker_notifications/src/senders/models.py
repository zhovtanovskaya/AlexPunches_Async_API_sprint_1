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
    user_info: UserInfoModel


class WelcomeEmailPosting(PostingBaseModel):
    """Модель отправления приветственного письма."""

    def is_ready(self):
        return self.is_actual()

    def is_actual(self) -> bool:
        """Проверить что сообщение актуально."""
        return self.posting.deadline > datetime.now()

    def is_daytime(self) -> bool:
        """Проверить что сейчас ночь в часовом поясе получателя."""
        user_tz = ZoneInfo(self.user_info.timezone)
        return not is_night(datetime.now(tz=user_tz))
