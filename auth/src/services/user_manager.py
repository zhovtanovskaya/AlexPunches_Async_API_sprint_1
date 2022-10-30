from functools import lru_cache
from typing import Type

from flask_security.datastore import SQLAlchemyUserDatastore

from core.db import db


class UserManagerService:
    """
    Класс управления пользователями.
    Регистрировать, назначать роли, хешировать пароли и т.д.
    """
    def __init__(self, user_model: Type[db.Model], role_model: Type[db.Model]):
        self.executor = SQLAlchemyUserDatastore(
            db=db, user_model=user_model, role_model=role_model
        )

    def create_user(self,
                    email: str,
                    password: str,
                    login: str | None = None,
                    is_superuser: bool = False,
                    ) -> db.Model:
        """Создать пользователя.
        Именно создать, а НЕ зарегистрировать.
        https://flask-security-too.readthedocs.io/en/stable/api.html#flask_security.UserDatastore.create_user
        """
        return self.executor.create_user(
            login=login,
            email=email,
            password=password,
            is_superuser=is_superuser,
        )


@lru_cache()
def get_user_manager_service(user_model: Type[db.Model],
                             role_model: Type[db.Model]
                             ) -> UserManagerService:
    return UserManagerService(user_model=user_model, role_model=role_model)
