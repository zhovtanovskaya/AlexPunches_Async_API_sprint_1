from functools import lru_cache

from core.config import config
from core.db import db
from models.schemes.users import UserCreateScheme, UserEditScheme
from services.user_manager import get_user_manager_service
from services.user_role import get_user_role_service


class UserService:
    """Класс управления пользователя."""

    def __init__(self):
        self.manager = get_user_manager_service(user_model=config.user_model,
                                                role_model=config.role_model)
        self.user_role_service = get_user_role_service()

    def register_user(self, user_in: UserCreateScheme) -> db.Model:
        """Регистрация пользователя."""
        return self.manager.register_user(user_scheme=user_in)

    def edit_user(self,
                  user_obj: config.user_model,
                  user_in: UserEditScheme,
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
