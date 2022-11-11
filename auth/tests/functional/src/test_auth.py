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
    'user, expected_response',
    [
        (
         faker_data.users[0],
         {'status': HTTPStatus.OK},
        ),
    ],
)
def test_signin(
        db_insert_fake_data,
        pg_cursor,
        http_client,
        user,
        expected_response,
        ):
    """Тест получения JWT к API."""
    response = http_client.post(
        url=test_settings.signin_endpoint,
        payload={'email': user.email, 'password': user.password},
    )
    response_json = response.json()

    assert response.status_code == expected_response['status']
    assert tuple(response_json.keys()) == ('access_token', 'refresh_token')


@pytest.mark.parametrize('user', [faker_data.users[0], faker_data.users[50]])
def test_signout(db_insert_fake_data, http_client, user):
    """Тест отзыва JWT.

    Сначала получаем рефреш-токен через АПИ, потом тестируем его отзыв отзыв.
    Получение токена проверяется в другом тесте -- test_signin().
    """
    # получить
    response_json = http_client.post(
        url=test_settings.signin_endpoint,
        payload={'email': user.email, 'password': user.password},
    ).json()
    r_refresh_token = response_json.get('refresh_token')

    # отозвать
    response = http_client.post(
        url=test_settings.signout_endpoint,
        headers={'Authorization': f'Bearer {r_refresh_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    # assert TODO чекнуть Редис


@pytest.mark.parametrize('user', [faker_data.users[20], faker_data.users[40]])
def test_refresh(db_insert_fake_data, user_action, user):
    """Тест обновления пары JWT."""
    response = user_action.login(email=user.email, password=user.password)
    r_refresh_token = response.json().get('refresh_token')
    headers = {'Authorization': f'Bearer {r_refresh_token}'}

    response_json = user_action.refresh(headers=headers).json()

    assert tuple(response_json.keys()) == ('access_token', 'refresh_token')
