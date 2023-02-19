from datetime import datetime, tzinfo

from pydantic import BaseModel, EmailStr

from core.config import config


class UserInfoModel(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    timezone: str = config.def_timezone


class PostingBaseModel(BaseModel):
    deadline: datetime
    user_info: UserInfoModel


class WelcomeEmailPosting(PostingBaseModel):
    pass
