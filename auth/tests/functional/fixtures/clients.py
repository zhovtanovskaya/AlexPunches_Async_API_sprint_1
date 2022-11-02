"""Фикстуры клиентов."""

import psycopg2
from psycopg2.extras import DictCursor
from typing import Any

import aiohttp
import aioredis
import pytest_asyncio
from functional.settings import test_settings


@pytest_asyncio.fixture(scope='function')
async def aiohttp_get():
    """Клиент aiohttp для тестирования API."""
    async def inner(url: str,
                    headers: dict | None = None,
                    params: dict | None = None,
                    ) -> dict[str, Any]:
        """Отправить GET запрос и получить ответ."""
        session = aiohttp.ClientSession(headers=headers)
        async with session.get(url, params=params) as response:
            body = await response.json()
            _headers = response.headers
            status = response.status
        await session.close()
        return {'body': body, 'headers': _headers, 'status': status}
    return inner


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    """Получить клиент Редиса перед сессией и закрыть его в конце сессии."""
    _client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    yield _client
    _client.close()
    await _client.wait_closed()


@pytest_asyncio.fixture(scope='session')
def conn_db():
    """Подключение к БД."""
    with psycopg2.connect(
                          dbname=test_settings.pg_settings.db_name,
                          user=test_settings.pg_settings.username,
                          password=test_settings.pg_settings.password,
                          host=test_settings.pg_settings.host,
                          port=test_settings.pg_settings.port,
                          cursor_factory=DictCursor,
                          async_=True,
                          ) as pg_conn:
        pg_cursor = pg_conn.cursor()
        yield pg_cursor
