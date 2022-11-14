"""Тесты Пользователя."""
from http import HTTPStatus

import pytest

from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


@pytest.mark.parametrize('user', [faker_data.users[0]])
def test_user_detail(db_insert_fake_data, admin_action, pg_cursor, user):
    """Детальная информация о пользователе корректная."""
    response = admin_action.get_user_detail(user_id=user.id)
    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == user.email


@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_user_after_edit_response(db_insert_fake_data,
                                  admin_action,
                                  pg_cursor,
                                  user,
                                  ):
    """После редактирования получаем корректный ответ с новыми данными."""
    new_email = 'aaa@aaa.aa'
    payload = {'email': new_email}

    response = admin_action.edit_user(user_id=user.id, payload=payload)
    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == new_email


@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_user_edit(db_insert_fake_data, admin_action, pg_cursor, user):
    """Данные ползователя редактируются корректно."""
    new_email = 'aaa@aaa.aa'
    payload = {'email': new_email}

    response = admin_action.edit_user(user_id=user.id, payload=payload)
    pg_stmt = f'SELECT * FROM {test_settings.users_tablename} '
    pg_stmt += f"WHERE id = '{faker_data.users[10].id}';"
    pg_cursor.execute(pg_stmt)
    count_obj = pg_cursor.fetchall()

    assert response.status_code == HTTPStatus.OK
    assert len(count_obj) == 1
    assert count_obj[0]['email'] == new_email
