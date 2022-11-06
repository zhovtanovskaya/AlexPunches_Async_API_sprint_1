from functools import lru_cache
from typing import Type

from core.db import db


class LoginHistoryManagerService:
    """
    Класс управления историей пользователей.
    Создавать, получать полный список, получить по конкретному id.
    """
    def __init__(self, login_history_model: Type[db.Model]):
        self.login_history_model = login_history_model

    def create_history(self, **kwargs) -> db.Model:
        """Создать историю пользователя.
        """
        login_history = self.login_history_model(**kwargs)
        db.session.add(login_history)
        login_history.save()

        return login_history


@lru_cache()
def get_login_history_manager_service(login_history_model: Type[db.Model],
                                      ) -> LoginHistoryManagerService:
    return LoginHistoryManagerService(login_history_model=login_history_model)
