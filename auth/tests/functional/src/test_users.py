"""Тесты Пользователя."""
from http import HTTPStatus

import pytest
import requests
from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


@pytest.mark.skip(reason='нужны эндпоинты users')
@pytest.mark.parametrize('user', [faker_data.users[0]])
def test_user_detail(db_insert_fake_data, pg_cursor, user):
    """Детальная информация о пользователе корректная."""
    url = test_settings.service_url
    url += '/api/v1/users/{user_id}/'.format(user_id=user.id)
    response = requests.get(url)

    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == user.email
    assert r_user.get('login') == user.login