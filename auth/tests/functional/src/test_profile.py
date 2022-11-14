"""Тесты Профиля."""
from http import HTTPStatus

import pytest

from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data
from functional.utils.user_action import UserActions

faker_data = get_faker_data()


@pytest.mark.parametrize('user', [faker_data.users[0], faker_data.users[10]])
def test_profile_detail(db_insert_fake_data, user_action, pg_cursor, user):
    """Детальная информация профиля корректная."""
    response = user_action.login(email=user.email, password=user.password)
    r_access_token = response.json().get('access_token')
    auth_user_action = UserActions(bearer=r_access_token)

    response = auth_user_action.get_profile()
    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == user.email


@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_profile_after_edit_response(db_insert_fake_data,
                                     user_action,
                                     pg_cursor,
                                     user,
                                     ):
    """После редактирования получаем корректный ответ с новыми данными."""
    response = user_action.login(email=user.email, password=user.password)
    r_access_token = response.json().get('access_token')
    auth_user_action = UserActions(bearer=r_access_token)
    new_email = 'aaa@aaa.aa'
    payload = {'email': new_email}

    response = auth_user_action.edit_profile(payload=payload)
    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == new_email


@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_profile_edit(db_insert_fake_data, user_action, pg_cursor, user):
    """Данные ползователя редактируются корректно."""
    response = user_action.login(email=user.email, password=user.password)
    r_access_token = response.json().get('access_token')
    auth_user_action = UserActions(bearer=r_access_token)
    new_email = 'aaa@aaa.aa'
    payload = {'email': new_email}

    response = auth_user_action.edit_profile(payload=payload)
    pg_stmt = f'SELECT * FROM {test_settings.users_tablename} '
    pg_stmt += f"WHERE id = '{faker_data.users[10].id}';"
    pg_cursor.execute(pg_stmt)
    count_obj = pg_cursor.fetchall()

    assert response.status_code == HTTPStatus.OK
    assert len(count_obj) == 1
    assert count_obj[0]['email'] == new_email


@pytest.mark.parametrize('user', [faker_data.users[0]])
def test_profile_singins(db_insert_fake_data, user_action, pg_cursor, user):
    """Данные ползователя редактируются корректно."""
    response = user_action.login(email=user.email, password=user.password)
    r_access_token = response.json().get('access_token')
    auth_user_action = UserActions(bearer=r_access_token)

    response = auth_user_action.get_profile_login_histories(per_page=4)
    login_history = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(login_history.get('login_histories')) == 4
    assert login_history.get('total_items') == 10
