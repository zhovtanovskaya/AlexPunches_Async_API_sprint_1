import pytest
from functional.settings import test_settings


@pytest.fixture(scope='function')
def redis_clear_data(redis_client):
    """Очистить кеш Редиса."""
    async def inner():
        await redis_client.flushall()
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
    es_index = test_settings.es_indexes['movies']
    await redis_clear_data()
    await es_write_data(data=es_determination_data['films'], es_index=es_index)

    url = test_settings.service_url + '/api/v1/films/'

    before_clean_es_response = await aiohttp_get(url=url)
    await es_clear_data(es_index=es_index)
    after_clean_es_response = await aiohttp_get(url=url)

    assert before_clean_es_response['status'] == 200
    assert after_clean_es_response['status'] == 200
    assert len(after_clean_es_response['body']) == 10
    assert before_clean_es_response['body'] == after_clean_es_response['body']
    assert after_clean_es_response['headers']['X-From-Redis-Cache'] == 'True'


@pytest.mark.asyncio
async def test_cache_film_with_header(
          es_write_data,
          es_determination_data,
          aiohttp_get,
          es_clear_data,
):
    """НЕ кешируется список фильмов, С заголовком 'X-Not-Cache'."""
    es_index = test_settings.es_indexes['movies']
    await es_write_data(data=es_determination_data['films'], es_index=es_index)

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'

    before_clean_es_response = await aiohttp_get(url=url, headers=headers)
    cleaner = await es_clear_data(es_index=es_index)
    after_clean_es_response = await aiohttp_get(url=url, headers=headers)

    assert before_clean_es_response['status'] == 200
    assert after_clean_es_response['status'] == 200
    assert len(before_clean_es_response['body']) == 10
    assert cleaner['deleted'] == 10
    assert len(after_clean_es_response['body']) == 0
