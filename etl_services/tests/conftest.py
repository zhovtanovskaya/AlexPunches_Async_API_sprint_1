import os
import sqlite3
import sys
from contextlib import contextmanager

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv('config/.env')

dsl = {
    'dbname':    os.environ.get('POSTGRES_DB_ADMIN'),
    'user':      os.environ.get('POSTGRES_USER_ADMIN'),
    'password':  os.environ.get('POSTGRES_PASSWORD_ADMIN'),
    'host':      os.environ.get('DB_HOST_ADMIN', '127.0.0.1'),
    'port':      os.environ.get('DB_PORT_ADMIN', 5432),
}
sqlite3_path = os.path.join(os.environ.get('SQLITE3_PATH'))


@contextmanager
def conn_context_sqlite3(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture()
def conn_db():
    """Подключение к БД."""
    with (
        conn_context_sqlite3(sqlite3_path) as sqlite_conn,
        psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn
    ):
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        yield sqlite_cursor, pg_cursor
