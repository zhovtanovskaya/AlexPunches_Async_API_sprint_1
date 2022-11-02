"""Сервис для управления пользвателями."""

from functools import lru_cache

from core.config import config
from core.db import db
from services.models.users import UserCreateModel, UserEditModel
from services.user_manager import get_user_manager_service


class UserService:
    """Класс управления пользователя."""

    def __init__(self):
        """Подключить UserManagerService."""
        self.manager = get_user_manager_service(user_model=config.user_model,
                                                role_model=config.role_model)

    def register_user(self, user_in: UserCreateModel) -> db.Model:
        """Регистрация пользователя."""
        return self.manager.register_user(user_scheme=user_in)

    def edit_user(self,
                  user_obj: config.user_model,
                  user_in: UserEditModel,
                  ) -> None:
        """Редактировать данные пользователя. !Кроме ролей."""
        user_obj.edit(scheme_in=user_in, exclude={'password'})
        if user_in.password is not None:
            self.manager.change_user_password(
                user_obj=user_obj,
                new_password=user_in.password,
            )


@lru_cache()
def get_user_service() -> UserService:
    """Создать и/или вернуть синглтон UserService."""
    return UserService()
