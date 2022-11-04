"""Фикстуры с данными."""
from psycopg2.extras import execute_batch
from typing import Generator

import functional.testdata.tables as ddl_tables
import pytest
from faker import Faker
from functional.settings import test_settings

fake = Faker()
Faker.seed(0)


@pytest.fixture(scope='session')
def create_tables(pg_conn, pg_cursor):
    """Создать таблицы БД."""
    pg_cursor.execute(ddl_tables.create_user)
    pg_cursor.execute(ddl_tables.create_roles)
    pg_cursor.execute(ddl_tables.create_roles_users)
    pg_conn.commit()
    yield
    pg_cursor.execute(ddl_tables.drop_roles_users)
    pg_cursor.execute(ddl_tables.drop_roles)
    pg_cursor.execute(ddl_tables.drop_user)


@pytest.fixture
def db_insert_fake_data(pg_conn,
                        pg_cursor,
                        create_tables,
                        ) -> Generator[None, None, None]:
    """Заполнить таблицы фейковыми данными."""
    query = """
    INSERT 
    INTO {users_tablename} (id, email, login, active, password, fs_uniquifier) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """.format(users_tablename=test_settings.users_tablename)  # noqa

    data = [(
        fake.uuid4(),
        fake.email(),
        fake.user_name(),
        fake.pybool(),
        fake.password(length=10),
        fake.pystr(),
    ) for _ in range(10)]
    execute_batch(pg_cursor, query, data)
    pg_conn.commit()
    yield
    pg_cursor.execute('truncate table {users_tablename} cascade;'.format(
        users_tablename=test_settings.users_tablename,
    ))
    pg_cursor.execute('truncate table {roles_tablename} cascade;'.format(
        roles_tablename=test_settings.roles_tablename,
    ))
    pg_cursor.execute('truncate table {roles_users_tablename} cascade;'.format(
        roles_users_tablename=test_settings.roles_users_tablename,
    ))
    pg_conn.commit()
