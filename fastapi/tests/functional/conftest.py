import asyncio
import os
import sys
from typing import Any

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from functional.settings import EsIndex, test_settings
from functional.testdata import determination_data, faker_films
from utils.helpers import orjson_dumps


def create_es_bulk_query(es_data, es_index: str, es_id_field: str):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            orjson_dumps({'index': {'_index': es_index, '_id': row[es_id_field]}}),  # noqa
            orjson_dumps(row)
        ])
    return bulk_query


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


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


@pytest_asyncio.fixture(scope='session')
async def es_client():
    """Получить клиент Эластика перед сессией
    и закрыть его в конце сессии."""
    client = AsyncElasticsearch(hosts=test_settings.es_url)
    for es_index in test_settings.es_indexes.values():
        await client.indices.create(
                index=es_index.name,
                body={'settings': es_index.setting,
                      'mappings': es_index.mapping},
            )
    yield client
    for es_index in test_settings.es_indexes.values():
        await client.indices.delete(index=es_index.name)
    await client.close()


@pytest.fixture
def es_write_data(es_client, es_clear_data):
    """Записать данные в Эластик."""
    async def inner(data: list[dict], es_index: EsIndex) -> None:
        await es_clear_data(es_index=es_index)
        if not data:
            return None
        bulk_query = create_es_bulk_query(data,
                                          es_index.name,
                                          es_index.id_field,
                                          )
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(operations=str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_clear_data(es_client):
    """Удалить все объекты из индекса в Эластике."""
    async def inner(es_index: EsIndex):
        return await es_client.delete_by_query(
            index=es_index.name,
            body={'query': {'match_all': {}}},
            refresh='true',
        )
    return inner


@pytest.fixture
def es_determination_data() -> dict:
    """Подготовить заранее определенные конкретные данные.
    :return: dict(
                 films: list,     # 10 штук
                 genres: list,    # 10 штук
                 persons: list,   # 10 штук
                )
    """
    return {
        'genres': determination_data.genres,
        'persons': determination_data.persons,
        'films': determination_data.films,
    }


@pytest.fixture
def es_fake_data_fix_count(faker) -> dict:
    """Подготовить фейковые данные в определенном количестве.
    :return: dict(
                 genres: list,    # 100 штук
                 persons: list,   # 100 штук
                 films: list,     # 1000 штук
                )
    """
    fake_films = faker_films.FakerFilms(
        genre_count=10 ** 2,
        person_count=10 ** 2,
        film_count=10 ** 3,
    )
    return {
        'genres': fake_films.genres,
        'persons': fake_films.persons,
        'films': fake_films.films,
    }
