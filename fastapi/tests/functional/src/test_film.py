"""
/api/v1/films?sort=-imdb_rating&page[size]=50&page[number]=1
Сортировка по рейтингу по убыванию работает
/api/v1/films?sort=imdb_rating&page[size]=50&page[number]=1
Сортировка по рейтингу по возрастанию работает

/api/v1/films?sort=-imdb_rating&filter[genre]=<comedy-uuid>
Фильтрация по жанру работает.
/api/v1/films?filter[genre]=<uuid:UUID>&sort=-imdb_rating&page[size]=50&page[number]=1
Пагинация на списках фильмов работает.
    размер и количество страниц корректное

/api/v1/films/search?query=captain&page[number]=1&page[size]=50
Поиск по фильмам работает корректно.
Пагинация на поиске работает корректно.
"""
import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'expected_answer',
    [
        {'status': 200, 'length': 10}
    ]
)
# @pytest.mark.skipif(True, reason="Api not ready")
@pytest.mark.asyncio
async def test_list_films(
          es_write_data,
          es_determination_data,
          expected_answer,
          aiohttp_get,
):
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'
    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


# /api/v1/films?sort=-imdb_rating&page[size]=50&page[number]=1
@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'sort': '-imdb_rating', 'page[size]': '50', 'page[number]': '1'},
            {'status': 200, 'length': 1}
        ),
        (
            {'sort': 'imdb_rating'}, {'status': 200, 'length': 2}
        )
    ]
)
# @pytest.mark.skipif(True, reason="Api not ready")
@pytest.mark.asyncio
async def test_sort_list_films(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)

    assert response['status'] == expected_answer['status']
