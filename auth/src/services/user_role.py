"""Сервис для управления сущностью Юзер-Роль."""

from functools import lru_cache
from http import HTTPStatus

from core.config import config
from core.db import db
from core.exceptions import ResourceNotFoundError
from services.user_manager import get_user_manager_service
from utils import messages as msg


class UserRoleService:
    """Класс управляет сущностью Юзер-Роль."""

    def __init__(self):
        """Подключить UserManagerService."""
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
        if not role:
            raise ResourceNotFoundError(
                msg.role_not_found_error, HTTPStatus.NOT_FOUND)
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
        if not role:
            raise ResourceNotFoundError(
                msg.role_not_found_error, HTTPStatus.NOT_FOUND)
        self.remove_user_role(user_obj=user, role_obj=role)

    def remove_user_role(self,
                         user_obj: config.user_model,
                         role_obj: config.role_model,
                         ) -> bool:
        """Отнять у пользователя Роль, передав объекты Пользователя и Роли."""
        return self.user_manager.remove_role_from_user(
            user=user_obj, role=role_obj,
        )

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
