"""Тесты энпоинтов для сущностей Юзер."""

import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'table, count',
    [(test_settings.users_tablename, 10), (test_settings.roles_tablename, 0)],
)
def test_test(db_insert_fake_data, pg_cursor, table: str, count: int):
    """Тестовый тест."""
    pg_stmt = 'SELECT COUNT(*) FROM {table} ;'.format(table=table)
    pg_cursor.execute(pg_stmt)

    count_obj = pg_cursor.fetchone()[0]

    assert count == count_obj


@pytest.mark.parametrize(
    'table, count',
    [(test_settings.users_tablename, 10), (test_settings.roles_tablename, 0)],
)
def test_user_detail(db_insert_fake_data, pg_cursor, table: str, count: int):
    """Тестовый тест."""
    pg_stmt = 'SELECT COUNT(*) FROM {table} ;'.format(table=table)
    pg_cursor.execute(pg_stmt)

    count_obj = pg_cursor.fetchone()[0]

    assert count == count_obj
