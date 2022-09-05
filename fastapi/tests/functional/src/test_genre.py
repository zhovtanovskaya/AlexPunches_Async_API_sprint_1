"""

/api/v1/genres/
Получаем все жанры.

/api/v1/genres/<uuid:UUID>/
Получаем конкретный жанр по ID.
Получаем 404, когда запрашиваем несуществующий жанр.
"""
import pytest
from functional.settings import test_settings


@pytest.mark.asyncio
async def test_list_genres(
          es_write_data,
          es_fake_data_fix_count,
          aiohttp_get,
):
    await es_write_data(
        data=es_fake_data_fix_count['genres'],
        es_index=test_settings.es_indexes['genres']
    )
    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/genres/'

    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == 200
    assert len(response['body']) == 100
