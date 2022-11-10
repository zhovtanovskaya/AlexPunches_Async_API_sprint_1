"""Тесты аутентификации."""
from http import HTTPStatus

import pytest

from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


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
         {'username': faker_data.users[0].login, 'password': 'pwd'},
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
    response = http_client.post(
        url=test_settings.signin_endpoint,
        payload=credentials,
    )
    response_json = response.json()
    assert tuple(response_json.keys()) == ('access_token', 'refresh_token')