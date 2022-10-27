from functools import lru_cache
from typing import Type

from core.db import db
from flask_security.datastore import SQLAlchemyUserDatastore


class UserManagerService:
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
