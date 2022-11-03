from datetime import datetime
from functools import lru_cache
from typing import Type

from flask_security.datastore import SQLAlchemyUserDatastore

from core.db import db


class LoginHistoryManagerService:
    """
    Класс управления историей пользователей.
    Создавать, получать полный список, получить по конкретному id.
    """
    def __init__(self, login_history_model: Type[db.Model]):
        self.executor = SQLAlchemyUserDatastore(
            db=db,
            login_history_model=login_history_model,
        )

    def create_history(
                    self,
                    user_name: str,
                    email: str,
                    data_create: datetime,
                    data_login: datetime,
                    ) -> db.Model:
        """Создать историю пользователя.
        """
        return self.executor.create_history(
            user_name=user_name,
            email=email,
            data_create=data_create,
            data_login=data_login,
        )


@lru_cache()
def get_login_history_manager_service(login_history_model: Type[db.Model],
                                      ) -> LoginHistoryManagerService:
    return LoginHistoryManagerService(login_history_model=login_history_model)
