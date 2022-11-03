"""Сервис для управления пользвателями."""

from functools import lru_cache

from core.config import config
from services.login_history import get_login_history_manager_service


class LoginHistoryService:
    """Класс управления пользователя."""

    def __init__(self):
        """Подключить LoginHistoryService."""
        self.manager = get_login_history_manager_service(
            login_history_model=config.login_history_model,
        )


@lru_cache()
def get_login_history_service() -> LoginHistoryService:
    """Создать и/или вернуть синглтон LoginHistoryService."""
    return LoginHistoryService()
