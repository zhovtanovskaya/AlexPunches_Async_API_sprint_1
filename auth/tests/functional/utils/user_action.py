"""Действия пользователя. Выполняются в тестах."""
from typing import Any, MutableMapping

from functional.settings import test_settings
from functional.utils.http_client import HttpClient


class UserActions(object):
    """Класс инкапсулирует типичные действия пользователя."""

    def __init__(self, bearer: str | None = None):
        """Подключить крафтовый http-клиент."""
        self.http_client = HttpClient(bearer=bearer)

    def register(self, username: str, password: str):
        """Зарегистрировать пользователя."""
        payload = {'email': username, 'password': password}
        return self.http_client.post(url=test_settings.signup_url,
                                     payload=payload,
                                     )

    def login(self, username: str, password: str):
        """Аутентифицировать пользователя."""
        return self.http_client.auth(url=test_settings.signin_url,
                                     username=username,
                                     password=password,
                                     )

    def logout(self):
        """Логаут."""
        return self.http_client.post(url=test_settings.signout_url)

    def refresh(self, headers: MutableMapping[str, Any] | None = None):
        """Обновить токены."""
        return self.http_client.post(url=test_settings.refresh_url,
                                     headers=headers,
                                     )
