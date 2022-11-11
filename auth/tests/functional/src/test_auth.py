"""Тесты аутентификации."""
from http import HTTPStatus

import pytest

from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()
# Срок жизни этого refresh-токена до 2032 года.
refresh_token = (
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
    'eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODE3NzcxNCwianRpIjoiNWM5Y2ZiNzYtZGFjMS00'
    'ZDdlLThiOWItYmJmM2FlY2VmYmM2IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJnd2lsbGlh'
    'bXNAZXhhbXBsZS5jb20iLCJuYmYiOjE2NjgxNzc3MTQsImV4cCI6MTk3OTIxNzcxNCwiYWp0'
    'aSI6Ijc2MWJmNjRjLTlhOTMtNGViOC05NTI1LWU2OGQwYTNjNjIyNyIsInJvbGVzIjpbXX0.'
    '3YWcKtGH7ETAu3S3rheCogTg4KfUZMoW8cNLbi3g6yg'
)


@pytest.mark.parametrize(
    'new_user, expected_answer',
    [
        (
         # все OK
         {'username': 'zzzz@zzzz.zz', 'password': 'asfhasdf6asdfJJHHJsd7676w'},
         {'status_code': HTTPStatus.CREATED, 'count_users_after_reg': 1},
        ),
        (
         # плохой email
         {'username': 'zzzz', 'password': '1111'},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_users_after_reg': 0},
        ),
        (
         # пустой пароль
         {'username': 'zzzz@zzz.zz', 'password': ''},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_users_after_reg': 0},
        ),
        (
         # плохой пароль
         {'username': 'zzzz@zzz.zz', 'password': '       '},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_users_after_reg': 0},
        ),
        (
         # email занят
         {'username': faker_data.users[0].email, 'password': '---111---'},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_users_after_reg': 1},
        ),
    ],
)
def test_user_registration(db_insert_fake_data,
                           pg_cursor,
                           user_action,
                           new_user,
                           expected_answer,
                           ):
    """Регистрация пользователя работает корректно."""
    response = user_action.register(username=new_user['username'],
                                    password=new_user['password'],
                                    )
    pg_stmt = f'SELECT COUNT(*) FROM {test_settings.users_tablename} '
    pg_stmt += f"WHERE email = '{new_user['username']}' ;"
    pg_cursor.execute(pg_stmt)

    count_obj = pg_cursor.fetchone()[0]

    assert response.status_code == expected_answer['status_code']
    assert count_obj == expected_answer['count_users_after_reg']


@pytest.mark.parametrize(
    'credentials, expected_response',
    [
        (
         {'email': faker_data.users[0].email, 'password': 'password'},
         {'status': HTTPStatus.OK, 'count_users_after_reg': 1},
        ),
    ],
)
def test_signin(
        db_insert_fake_data,
        pg_cursor,
        http_client,
        credentials,
        expected_response,
        ):
    """Тест получения JWT к API."""
    response = http_client.post(
        url=test_settings.signin_endpoint,
        payload=credentials,
    )
    assert response.status_code == expected_response['status'], response.json()
    response_json = response.json()
    assert tuple(response_json.keys()) == ('access_token', 'refresh_token'), response_json


def test_signout(http_client):
    """Тест отзыва JWT."""
    response = http_client.post(
        url=test_settings.signout_endpoint,
        headers={'Authorization': f'Bearer {refresh_token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_refresh(http_client):
    """Тест обновления пары JWT."""
    response = http_client.post(
        url=test_settings.refresh_endpoint,
        headers={'Authorization': f'Bearer {refresh_token}'},
    )
    response_json = response.json()
    assert tuple(response_json.keys()) == ('access_token', 'refresh_token'), response_json

