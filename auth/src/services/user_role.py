from functools import lru_cache

from core.config import config
from core.db import db
from services.user_manager import get_user_manager_service


class UserRoleService:
    """Класс управляет сущностью Юзер-Роль."""

    def __init__(self):
        self.user_manager = get_user_manager_service(
            user_model=config.user_model,
            role_model=config.role_model,
        )

    def create_user_role_by_rolename(self,
                                     user: config.user_model,
                                     rolename: str,
                                     ) -> None:
        """Добавить пользователю Роль по названию Роли."""
        role = self._get_role_by_rolename(rolename=rolename)
        self.create_user_role(user=user, role=role)

    def create_user_role(self,
                         user: config.user_model,
                         role: config.role_model,
                         ) -> None:
        """Добавить пользователю роль, передав объекты Пользователя и Роли."""
        self.user_manager.add_role_to_user(user=user, role=role)

    def remove_user_role_by_rolename(self,
                                     user: config.user_model,
                                     rolename: str,
                                     ) -> None:
        """Отнять у пользователя Роль по названию Роли."""
        role = self._get_role_by_rolename(rolename=rolename)
        self.remove_user_role(user=user, role=role)

    def remove_user_role(self,
                         user: config.user_model,
                         role: config.role_model,
                         ) -> None:
        """Отнять у пользователя Роль, передав объекты Пользователя и Роли."""
        self.user_manager.remove_role_from_user(user=user, role=role)

    @staticmethod
    def _get_role_by_rolename(rolename: str) -> config.role_model:
        """Получить Роль по названию."""
        return db.session.query(config.role_model).filter(
            config.role_model.name == rolename,
        ).first()


@lru_cache()
def get_user_role_service() -> UserRoleService:
    """Создать и/или вернуть синглтон UserRoleService."""
    return UserRoleService()
