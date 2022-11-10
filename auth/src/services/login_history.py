"""Модуль уравления историей входов пользователей."""
from functools import lru_cache

import services.models.login_histories as service_models
from models import LoginHistory


class LoginHistoryService:
    """Класс управления историей пользователей.

    Создавать, получать полный список, получить по конкретному id.
    """

    login_history_model = LoginHistory

    def create_history(self,
                       login_history: service_models.LoginHistoryCreateModel,
                       ) -> service_models.LoginHistoryModel:
        """Добавить запись в историю пользователя."""
        singin = LoginHistory(**login_history.dict())
        singin.create()
        return service_models.LoginHistoryModel.from_orm(singin)


@lru_cache()
def get_login_history_service() -> LoginHistoryService:
    """Синглтон."""
    return LoginHistoryService()
