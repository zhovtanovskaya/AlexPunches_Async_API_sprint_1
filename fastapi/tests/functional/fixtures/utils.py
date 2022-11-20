import asyncio

import pytest

from functional.settings import EsIndex
from functional.utils.helpers import orjson_dumps


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
            query={'match_all': {}},
            refresh='true',
        )
    return inner
