"""Вспомогательные полезные действия. Выполняются в тестах."""
from functools import lru_cache
from typing import Any, Mapping, MutableMapping

import requests
from requests import Response
from requests.auth import HTTPBasicAuth


class HttpClient:
    """Клиент, который оправляет  http-запросы к API."""

    def __init__(self, bearer: str | None = None) -> None:
        """Подключить requests и Добавить заголовок авторизации."""
        self.headers = {'accept': 'application/json'}
        self._client = requests
        if bearer:
            self.headers['Authorization'] = f'Bearer {bearer}'

    def get(self,
            url: str,
            headers: MutableMapping[str, str] | None = None,
            payload: Mapping[str, Any] | None = None,
            ) -> Response:
        """Отправить GET-запрос и получить ответ."""
        if headers:
            self.headers = headers
        return self._client.get(url=url, headers=self.headers, params=payload)

    def post(self,
             url: str,
             headers: MutableMapping[str, str] | None = None,
             payload: Mapping[str, Any] | None = None,
             ) -> Response:
        """Отправить POST-запрос и получить ответ."""
        if headers:
            self.headers = headers
        return self._client.post(url=url, headers=self.headers, json=payload)

    def patch(self,
              url: str,
              headers: MutableMapping[str, str] | None = None,
              payload: Mapping[str, Any] | None = None,
              ) -> Response:
        """Отправить PATCH-запрос и получить ответ."""
        if headers:
            self.headers = headers
        return self._client.patch(url=url, headers=self.headers, json=payload)

    def delete(self, url: str) -> Response:
        """Отправить DELETE-запрос и получить ответ."""
        return self._client.delete(url=url)

    def auth(self, url: str, username: str, password: str) -> Response:
        """Аутентифицироваться через HTTPBasic и получить ответ."""
        basic = HTTPBasicAuth(username, password)
        return self._client.get(url=url, auth=basic)


@lru_cache()
def get_http_client() -> HttpClient:
    """Сделать синглтоном."""
    return HttpClient()
