import asyncio
import datetime
import json
import os
import sys
import uuid

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from functional.settings import test_settings
from functional.testdata.es_mapping import (genre_mapping, movie_mappings,
                                            person_mapping)
from functional.testdata.es_setting import es_setting


def get_es_bulk_query(es_data, es_index, es_id_field):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': es_index, '_id': row[es_id_field]}}),  # noqa
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(
        hosts=test_settings.es_host,
        validate_cert=False,
        use_ssl=False
    )
    await client.indices.create(
            index=test_settings.es_index,
            body={'settings': es_setting, 'mappings': movie_mappings},
        )
    yield client
    await client.indices.delete(index=test_settings.es_index)
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(data, test_settings.es_index, test_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_clear_data(es_client):
    async def inner():

        await es_client.delete_by_query(
            index=test_settings.es_index,
            body={'query': {'match_all': {}}},
        )
    return inner


@pytest.fixture
def es_data():
    id_1 = str(uuid.uuid4())
    id_2 = str(uuid.uuid4())
    id_3 = str(uuid.uuid4())
    id_4 = str(uuid.uuid4())
    return [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': id_1, 'name': 'Ann'},
            {'id': id_2, 'name': 'Bob'}
        ],
        'writers': [
            {'id': id_3, 'name': 'Ben'},
            {'id': id_4, 'name': 'Howard'}
        ],
        # 'created_at': datetime.datetime.now().isoformat(),
        # 'updated_at': datetime.datetime.now().isoformat(),
        # 'film_work_type': 'movie'
    } for _ in range(60)]
