from typing import Any

import aiohttp
import aioredis
import pytest_asyncio
from functional.settings import test_settings


@pytest_asyncio.fixture(scope='function')
async def aiohttp_get():
    async def inner(url: str,
                    headers: dict | None = None,
                    params: dict | None = None,
                    ) -> dict[str, Any]:
        """"Отправить GET запрос и получить ответ."""
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
    """Получить клиент Редиса перед сессией
    и закрыть его в конце сессии."""
    _client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    yield _client
    _client.close()
    await _client.wait_closed()
