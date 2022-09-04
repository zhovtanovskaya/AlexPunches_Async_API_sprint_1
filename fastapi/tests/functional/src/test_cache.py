import pytest
from functional.settings import test_settings


@pytest.fixture(scope='function')
def redis_clear_data(redis_client):
    """Очистить кеш Редиса."""
    async def inner():
        redis_client.flushall()
    return inner


@pytest.mark.asyncio
async def test_cache_film_without_header(
          es_write_data,
          es_determination_data,
          aiohttp_get,
          redis_clear_data,
          es_clear_data,
):
    """Кешируется список фильмов, БЕЗ заголовка 'X-Not-Cache'."""
    await redis_clear_data()
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_index,
        es_id_field=test_settings.es_id_field,
    )

    url = test_settings.service_url + '/api/v1/films/'

    first_response = await aiohttp_get(url=url)

    await es_clear_data()

    after_es_clear_response = await aiohttp_get(url=url)

    assert first_response['status'] == 200
    assert after_es_clear_response['status'] == 200
    assert first_response['body'] == after_es_clear_response['body']


@pytest.mark.asyncio
async def test_cache_film_with_header(
          es_write_data,
          es_determination_data,
          aiohttp_get,
          es_clear_data,
):
    """НЕ кешируется список фильмов, С заголовком 'X-Not-Cache'."""
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_index,
        es_id_field=test_settings.es_id_field,
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'

    first_response = await aiohttp_get(url=url, headers=headers)
    cleaner = await es_clear_data()
    after_es_clear_response = await aiohttp_get(url=url, headers=headers)

    assert first_response['status'] == 200
    assert after_es_clear_response['status'] == 200
    assert len(first_response['body']) == 10
    assert cleaner['deleted'] == 10
    assert len(after_es_clear_response['body']) == 0
