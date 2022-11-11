"""Тесты Пользователя."""
from http import HTTPStatus

import pytest

from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


@pytest.mark.parametrize('role', [faker_data.roles[0]])
def test_role_detail(db_insert_fake_data, user_action, pg_cursor, role):
    """Детальная информация о Роли корректная."""
    response = user_action.get_role_detail(role_id=role.id)
    r_role = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_role.get('name') == role.name
    assert r_role.get('description') == role.description


@pytest.mark.parametrize('role', [faker_data.roles[5]])
def test_role_after_edit_response(db_insert_fake_data,
                                  user_action,
                                  pg_cursor,
                                  role,
                                  ):
    """После редактирования получаем корректный ответ с новыми данными."""
    new_name = 'rrroooollleee'
    new_description = 'Role descriptionRole descriptionRole description'
    payload = {'name': new_name, 'description': new_description}

    response = user_action.edit_role(role_id=role.id, payload=payload)
    r_role = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_role.get('description') == new_description
    assert r_role.get('name') == new_name


@pytest.mark.parametrize('role', [faker_data.roles[4]])
def test_role_edit(db_insert_fake_data, user_action, pg_cursor, role):
    """Данные Роли редактируются корректно."""
    new_name = 'rrroooollleee'
    new_description = 'Role descriptionRole descriptionRole description'
    payload = {'name': new_name, 'description': new_description}

    response = user_action.edit_role(role_id=role.id, payload=payload)
    pg_stmt = f'SELECT * FROM {test_settings.roles_tablename} '
    pg_stmt += f"WHERE id = '{faker_data.roles[4].id}';"
    pg_cursor.execute(pg_stmt)
    count_obj = pg_cursor.fetchall()

    assert response.status_code == HTTPStatus.OK
    assert len(count_obj) == 1
    assert count_obj[0]['description'] == new_description
    assert count_obj[0]['name'] == new_name


@pytest.mark.parametrize('roles', [faker_data.roles])
def test_list_roles(db_insert_fake_data, user_action, pg_cursor, roles):
    """Список Ролей корректныый."""
    response = user_action.get_roles()
    r_roles = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(r_roles.get('list_roles')) == len(roles)


# @pytest.mark.skip(reason='решить проблему с psycopg2.errors.UniqueViolation')
@pytest.mark.parametrize(
    'new_role, expected_answer',
    [
        (
         # все OK
         {'name': 'zzzznn', 'description': 'asfhasdf6asdfJJHHJsd7676w'},
         {'status_code': HTTPStatus.CREATED, 'count_roles_after_reg': 1},
        ),
        (
         # пустое название
         {'name': '', 'description': '1111'},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_roles_after_reg': 0},
        ),
        (
         # name занят
         {'name': faker_data.roles[0].name, 'description': '222222'},
         {'status_code': HTTPStatus.BAD_REQUEST, 'count_roles_after_reg': 1},
        ),
    ],
)
def test_add_role(
                  db_insert_fake_data,
                  pg_conn,
                  user_action,
                  new_role,
                  expected_answer,
                  ):
    """Регистрация пользователя работает корректно."""
    pg_cursor = pg_conn.cursor()
    response = user_action.add_role(payload=new_role)
    pg_stmt = f'SELECT COUNT(*) FROM {test_settings.roles_tablename} '
    pg_stmt += f"WHERE name = '{new_role['name']}' ;"
    pg_cursor.execute(pg_stmt)

    count_obj = pg_cursor.fetchone()[0]
    pg_cursor.close()

    assert response.status_code == expected_answer['status_code']
    assert count_obj == expected_answer['count_roles_after_reg']
