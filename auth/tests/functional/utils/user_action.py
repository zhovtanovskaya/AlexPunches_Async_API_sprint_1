"""Действия пользователя. Выполняются в тестах."""
from typing import Any, Mapping, MutableMapping

from requests import Response

from functional.settings import test_settings
from functional.utils.http_client import HttpClient


class UserActions(object):
    """Класс инкапсулирует типичные действия пользователя."""

    def __init__(self, bearer: str | None = None) -> Response:
        """Подключить крафтовый http-клиент."""
        self.http_client = HttpClient(bearer=bearer)

    def register(self, username: str, password: str) -> Response:
        """Зарегистрировать пользователя."""
        payload = {'email': username, 'password': password}
        return self.http_client.post(url=test_settings.signup_endpoint,
                                     payload=payload,
                                     )

    def login(self, email: str, password: str) -> Response:
        """Аутентифицировать пользователя."""
        payload = {'email': email, 'password': password}
        return self.http_client.post(url=test_settings.signin_endpoint,
                                     payload=payload,
                                     )

    def logout(self) -> Response:
        """Логаут."""
        return self.http_client.post(url=test_settings.signout_endpoint)

    def refresh(self,
                headers: MutableMapping[str, Any] | None = None,
                ) -> Response:
        """Обновить токены."""
        return self.http_client.post(url=test_settings.refresh_endpoint,
                                     headers=headers,
                                     )

    def edit_user(self,
                  user_id: str,
                  payload: Mapping[str, Any] | None = None,
                  ) -> Response:
        """Редактировать данные пользователя, частями. PATCH."""
        url = test_settings.service_url + test_settings.users_endpoint + f'/{user_id}/'  # noqa
        return self.http_client.patch(url=url, payload=payload)

    def get_user_detail(self, user_id: str) -> Response:
        """Получить детальные данные о пользователе."""
        url = test_settings.service_url + test_settings.users_endpoint + f'/{user_id}/'  # noqa
        return self.http_client.get(url=url)

    def get_user_login_histories(
            self, user_id: str, page_number: int, per_page: int,
            ) -> Response:
        url = (
                test_settings.service_url +
                test_settings.users_endpoint +
                f'/{user_id}/singins' +
                f'?page_number={page_number}&per_page={per_page}'
        )
        return self.http_client.get(url=url)

    def get_roles(self) -> Response:
        """Получить список Ролей."""
        url = test_settings.service_url + test_settings.roles_endpoint + '/'
        return self.http_client.get(url=url)

    def get_role_detail(self, role_id: int) -> Response:
        """Получить Роль."""
        url = test_settings.service_url + test_settings.roles_endpoint + f'/{role_id}/'  # noqa
        return self.http_client.get(url=url)

    def edit_role(self,
                  role_id: str,
                  payload: Mapping[str, Any] | None = None,
                  ) -> Response:
        """Редактировать данные пользователя, частями. PATCH."""
        url = test_settings.service_url + test_settings.roles_endpoint + f'/{role_id}/'  # noqa
        return self.http_client.patch(url=url, payload=payload)

    def add_role(self,
                 payload: Mapping[str, Any] | None = None,
                 ) -> Response:
        """Добавить Роль."""
        url = test_settings.service_url + test_settings.roles_endpoint + '/'
        return self.http_client.post(url=url, payload=payload)

    def get_profile(self) -> Response:
        """Получить детальные данные профиля для авторизованного юзера."""
        url = test_settings.service_url + test_settings.profile_endpoint
        return self.http_client.get(url=url)

    def edit_profile(self,
                     payload: Mapping[str, Any] | None = None,
                     ) -> Response:
        """Редактировать свои данные авторизованного юзера, частями. PATCH."""
        url = test_settings.service_url + test_settings.profile_endpoint
        return self.http_client.patch(url=url, payload=payload)

    def get_profile_login_histories(
            self, page_number: int | None = None, per_page: int | None = None,
            ) -> Response:
        url = (
               test_settings.service_url +
               test_settings.profile_endpoint + '/singins?'
        )
        if page_number:
            url += f'page_number={page_number}'
        if per_page:
            url += f'&per_page={per_page}'

        return self.http_client.get(url=url)
