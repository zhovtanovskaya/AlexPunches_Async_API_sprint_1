import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
         {'filter[genre]': 'f39d7b6d-aef2-40b1-aaf0-cf05e7048011', 'sort': '-imdb_rating', 'page[size]': '50', 'page[number]': '1'},
         {'status': 200, 'length': 6, 'ids': ['6c98f73d-27fe-4b4b-9bf1-f1d18b92c247', 'f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', '50852f4f-0b09-4c41-b89a-28298a663359', '6480fdc0-f1c5-4f44-be08-3c1bcda6a326']}
        ),
        (
         {'filter[genre]': '', 'sort': '-imdb_rating', 'page[size]': '50', 'page[number]': '1'},
         {'status': 200, 'length': 10, 'ids': ['e32866d3-0d6a-48b0-beda-9ab9bec60ffe', '6d4ba69c-d169-43f2-93bf-a9fe9cdd9f6c', '1a42b629-14af-4646-be32-16bd97d01e70', '6c98f73d-27fe-4b4b-9bf1-f1d18b92c247', 'f8db1a4d-584d-4c02-8ff9-d318d22a3a62', 'f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', '50852f4f-0b09-4c41-b89a-28298a663359', '6480fdc0-f1c5-4f44-be08-3c1bcda6a326']}
        ),
    ]
)
@pytest.mark.asyncio
async def test_list_films(
          es_write_data,
          es_determination_data,
          expected_answer,
          query_data,
          aiohttp_get,
):
    """
    Фильтрация по жанру работает.
    """
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)
    films_ids = [film['uuid'] for film in response['body']]

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
    assert films_ids == expected_answer['ids']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'sort': '-imdb_rating', 'page[size]': '50', 'page[number]': '1'},
            {'status': 200, 'length': 10, 'ids': ['e32866d3-0d6a-48b0-beda-9ab9bec60ffe', '6d4ba69c-d169-43f2-93bf-a9fe9cdd9f6c', '1a42b629-14af-4646-be32-16bd97d01e70', '6c98f73d-27fe-4b4b-9bf1-f1d18b92c247', 'f8db1a4d-584d-4c02-8ff9-d318d22a3a62', 'f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', '50852f4f-0b09-4c41-b89a-28298a663359', '6480fdc0-f1c5-4f44-be08-3c1bcda6a326']}
        ),
        (
            {'sort': 'imdb_rating'},
            {'status': 200, 'length': 10, 'ids': ['6480fdc0-f1c5-4f44-be08-3c1bcda6a326', '50852f4f-0b09-4c41-b89a-28298a663359', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', 'f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'f8db1a4d-584d-4c02-8ff9-d318d22a3a62', '6c98f73d-27fe-4b4b-9bf1-f1d18b92c247', '1a42b629-14af-4646-be32-16bd97d01e70', '6d4ba69c-d169-43f2-93bf-a9fe9cdd9f6c', 'e32866d3-0d6a-48b0-beda-9ab9bec60ffe']}
        )
    ]
)
@pytest.mark.asyncio
async def test_list_films_sort(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    """
    Сортировка по рейтингу по убыванию работает.
    Сортировка по рейтингу по возрастанию работает.
    """
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)
    films_ids = [film['uuid'] for film in response['body']]

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
    assert films_ids == expected_answer['ids']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'page[size]': '5', 'page[number]': '1'},
            {'status': 200, 'length': 5, 'ids': ['0b36f3cd-0acf-4ba4-8410-30ae56525ce0', '1a42b629-14af-4646-be32-16bd97d01e70', '50852f4f-0b09-4c41-b89a-28298a663359', '6480fdc0-f1c5-4f44-be08-3c1bcda6a326', '6c98f73d-27fe-4b4b-9bf1-f1d18b92c247']}
        ),
        (
            {'page[size]': '3', 'page[number]': '4'},
            {'status': 200, 'length': 1, 'ids': ['fdc12930-82ae-452f-ad40-76bcf9cb2ee8']}
        )
    ]
)
@pytest.mark.asyncio
async def test_list_films_pagination(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    """
    Пагинация на списках фильмов работает
        размер и количество страниц корректное.
    """
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)
    films_ids = [film['uuid'] for film in response['body']]

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
    assert films_ids == expected_answer['ids']
