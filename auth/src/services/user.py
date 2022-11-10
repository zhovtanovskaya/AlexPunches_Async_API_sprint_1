"""Сервис для управления пользвателями."""
from functools import lru_cache
from typing import Type
from uuid import UUID

from werkzeug.security import generate_password_hash

import services.models.roles as service_role_models
import services.models.users as service_user_models
from core.db import db
from models.role import Role
from models.user import User


class UserService:
    """Класс управления пользователя."""

    user_model: Type[db.Model] = User
    role_model: Type[db.Model] = Role

    def register_user(self,
                      user_in: service_user_models.UserCreateModel,
                      ) -> service_user_models.UserModel:
        """Зарегистрировать пользователя."""
        user_values = user_in.dict(
            exclude={'password'},
            exclude_unset=True,
        )
        user_values['password'] = generate_password_hash(
            password=user_in.password, method='sha256',
        )
        new_user = self.user_model(**user_values)
        new_user.create()
        return service_user_models.UserModel.from_orm(new_user)

    def get_user_by_id(self, id: UUID) -> service_user_models.UserModel:
        """Получить пользователя."""
        user = self.user_model.get_or_404(id=id)
        return service_user_models.UserModel.from_orm(user)

    def edit(self,
             user_in: service_user_models.UserEditModel,
             ) -> service_user_models.UserModel:
        """Редактировать данные пользователя. !Кроме ролей."""
        user = self.user_model.get_or_404(id=user_in.id)
        user.edit(scheme_in=user_in, exclude={'password', 'roles'})
        if user_in.password is not None:
            user.password = generate_password_hash(
                password=user_in.password, method='sha256',
            )
        user.save()
        return service_user_models.UserModel.from_orm(user)

    def get_user_roles_by_user_id(self,
                                  user_id: UUID,
                                  ) -> list[service_role_models.RoleModel]:
        """Получить список Ролей пользователя."""
        user = self.user_model.get_or_404(id=user_id)
        return [
            service_role_models.RoleModel.from_orm(role) for role in user.roles
        ]

    def remove_role_from_user(self, user_id: UUID, role_id: int) -> None:
        """Отобрать Роль у пользователя."""
        user = self.user_model.get_or_404(id=user_id)
        role = self.role_model.get_or_404(id=role_id)
        user.roles.remove(role)
        user.save()

    def add_role_to_user_by_rolename(self,
                                     user_id: UUID,
                                     rolename: str,
                                     ) -> bool:
        """Добавить пользователю Роль по названию Роли."""
        user = self.user_model.get_or_404(id=user_id)
        role = self.role_model.query.filter_by(name=rolename).first()
        if role in user.roles:
            return False
        return self._create_user_role_by_orm(user=user, role=role)

    @staticmethod
    def _create_user_role_by_orm(user: db.Model, role: db.Model) -> bool:
        """Добавить пользователю Роль. Используя Модели ОРМ."""
        user.roles.append(role)
        user.save()
        return True


@lru_cache()
def get_user_service() -> UserService:
    """Создать и/или вернуть синглтон UserService."""
    return UserService()
