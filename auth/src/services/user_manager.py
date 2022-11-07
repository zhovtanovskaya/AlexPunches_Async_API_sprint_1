"""Слой абстракции между сервисами и внешней либой (Flask-Security-Too)."""

from functools import lru_cache
from typing import Type

from flask_security import RegisterForm
from flask_security.changeable import change_user_password
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.registerable import register_user as security_register_user
from pydantic import BaseModel
from wtforms import StringField

from core.db import db


class ExtendedRegForm(RegisterForm):
    """Класс добавляет кастомные поля для "формы" регистрации."""

    username = StringField('Login')


class UserManagerService:
    """Класс облегчает разные действия над пользователями.

    Регистрировать, назначать роли, хешировать пароли и т.д.
    """

    def __init__(self,
                 user_model: Type[db.Model],
                 role_model: Type[db.Model],
                 ):
        """Подключаем внешнюю библиотеку Flask-Security-Too."""
        self.executor = SQLAlchemyUserDatastore(
            db=db, user_model=user_model, role_model=role_model,
        )

    @staticmethod
    def register_user(user_scheme: BaseModel) -> db.Model:
        """Зарегистрировать пользователя."""
        user_data = ExtendedRegForm(**user_scheme.dict())
        return security_register_user(user_data)

    def create_user(self,
                    email: str,
                    password: str,
                    login: str | None = None,
                    ) -> db.Model:
        """Создать пользователя.

        Именно создать, а НЕ зарегистрировать.
        https://flask-security-too.readthedocs.io/en/stable/api.html#flask_security.UserDatastore.create_user
        """
        return self.executor.create_user(
            login=login,
            email=email,
            password=password,
        )

    def add_role_to_user(self, user: db.Model, role: db.Model) -> bool:
        """Добавить Роль пользователю."""
        return self.executor.add_role_to_user(user=user, role=role)

    def remove_role_from_user(self, user: db.Model, role: db.Model) -> bool:
        """Удалить Роль у пользователя."""
        return self.executor.remove_role_from_user(user=user, role=role)

    def add_roles_to_user(self,
                          user: db.Model,
                          roles: list[db.Model],
                          ) -> None:
        """Добавить список ролей пользователю."""
        for role in roles:
            self.add_role_to_user(user=user, role=role)

    def remove_roles_from_user(self,
                               user: db.Model,
                               roles: list[db.Model],
                               ) -> None:
        """Удалить список ролей у пользователя."""
        for role in roles:
            self.remove_role_from_user(user=user, role=role)

    def find_or_create_role(self, name: str) -> db.Model:
        """Вернуть Роль по названию. Если несуществует -- создать и вернуть."""
        return self.executor.find_or_create_role(name=name)

    @staticmethod
    def change_user_password(user_obj: db.Model, new_password: str) -> None:
        """Изменить пароль у пользователя."""
        change_user_password(
            user=user_obj, password=new_password, notify=False)


@lru_cache()
def get_user_manager_service(user_model: Type[db.Model],
                             role_model: Type[db.Model],
                             ) -> UserManagerService:
    """Создать и/или вернуть синглтон UserManagerService."""
    return UserManagerService(user_model=user_model, role_model=role_model)
