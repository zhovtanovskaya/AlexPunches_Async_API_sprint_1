"""Фикстуры с данными."""
from typing import Generator

import pytest
from faker import Faker
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch

import functional.testdata.tables as ddl_tables
from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data
from functional.utils.helpers import construct_query

fake = Faker()
Faker.seed(0)


@pytest.fixture(scope='session')
def create_tables(pg_conn: _connection,
                  pg_cursor: DictCursor,
                  ) -> Generator[None, None, None]:
    """Создать таблицы БД."""
    pg_cursor.execute(ddl_tables.drop_roles_users)
    pg_cursor.execute(ddl_tables.drop_roles)
    pg_cursor.execute(ddl_tables.drop_user)
    pg_cursor.execute(ddl_tables.drop_login_histories)
    pg_cursor.execute(ddl_tables.create_user)
    pg_cursor.execute(ddl_tables.create_login_history)
    pg_cursor.execute(ddl_tables.create_roles)
    pg_cursor.execute(ddl_tables.create_roles_users)
    pg_conn.commit()
    yield
    pg_cursor.execute(ddl_tables.drop_roles_users)
    pg_cursor.execute(ddl_tables.drop_login_histories)
    pg_cursor.execute(ddl_tables.drop_roles)
    pg_cursor.execute(ddl_tables.drop_user)


@pytest.fixture(scope='function')
def db_insert_fake_data(pg_conn: _connection,
                        pg_cursor: DictCursor,
                        create_tables: None,
                        ) -> Generator[None, None, None]:
    """Заполнить таблицы фейковыми данными."""
    faker_data = get_faker_data()

    for _table_name, _data_class in test_settings.fake_data_map.items():
        _data = faker_data.get_data_by_table_name(table_name=_table_name)
        if _data is not None:
            stmt, data = construct_query(table_name=_table_name,
                                         data_class=_data_class,
                                         data=_data,
                                         )
            execute_batch(pg_cursor, stmt, data)

    pg_conn.commit()
    yield
    pg_cursor.execute(f'truncate table {test_settings.users_tablename} restart identity cascade;')  # noqa
    pg_cursor.execute(f'truncate table {test_settings.roles_tablename} restart identity cascade;')  # noqa
    pg_cursor.execute(f'truncate table {test_settings.roles_users_tablename} restart identity cascade;')  # noqa
    pg_cursor.execute(f'truncate table {test_settings.login_histories_tablename} restart identity cascade;')  # noqa
    pg_conn.commit()
