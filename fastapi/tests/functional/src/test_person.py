from http import HTTPStatus

import pytest
from functional.settings import test_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'path_param, expected_answer',
    [
        (
            {'person_uuid': '6c0be55c-90e6-49e1-a44f-c3a96d0c62c3'},
            {'status': HTTPStatus.OK,
                'length': 4,
                'film_ids': ['f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', 'e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
            {'person_uuid': '7f22cd12-07b6-408e-aac1-ca75afb918c8'},
            {'status': HTTPStatus.OK,
                'length': 1,
                'film_ids': ['e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
              {'person_uuid': '01af52ec-9345-4d66-adbe-50e54577434e'},
              {'status': HTTPStatus.NOT_FOUND, 'length': 0, 'film_ids': []}
        )
    ]
)
async def test_person_films(
          es_write_data,
          es_determination_data,
          path_param,
          expected_answer,
          aiohttp_get,
):
    """
    Получаем все фильмы, в которых есть персона. По ID персоны.
    """
    await es_write_data(
        data=es_determination_data['persons'],
        es_index=test_settings.es_indexes['persons']
    )

    headers = {'X-Not-Cache': 'True'}
    url = f"{test_settings.service_url}/api/v1/persons/{path_param['person_uuid']}/films"
    response = await aiohttp_get(url=url, headers=headers)
    films_ids = []
    if response['status'] == HTTPStatus.OK and type(response['body']) == list:
        films_ids = [film['uuid'] for film in response['body']]

    assert response['status'] == expected_answer['status']
    assert len(films_ids) == expected_answer['length']
    assert sorted(films_ids) == sorted(expected_answer.get('film_ids', []))


@pytest.mark.parametrize(
    'path_param, expected_answer',
    [
        (
            {'person_uuid': '6c0be55c-90e6-49e1-a44f-c3a96d0c62c3'},
            {'status': HTTPStatus.OK,
                'full_name': 'Taylor Perry',
                'role': ['director', 'actor', 'writer'],
                'film_ids': ['f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', 'e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
            {'person_uuid': '7f22cd12-07b6-408e-aac1-ca75afb918c8'},
            {'status': HTTPStatus.OK,
                'full_name': 'Tony a Sharp',
                'role': ['actor'],
                'film_ids': ['e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
              {'person_uuid': '01af52ec-9345-4d66-adbe-50e54577434e'},
              {'status': HTTPStatus.NOT_FOUND}
        )
    ]
)
async def test_person_detail(
          es_write_data,
          es_determination_data,
          path_param,
          expected_answer,
          aiohttp_get,
):
    """
    Получаем конкретную персону по ID.
    Получаем 404, когда передаем несуществующий ID.

    У Персоны корректный список фильмов.
    У Персоны корректный список role.
    """
    await es_write_data(
        data=es_determination_data['persons'],
        es_index=test_settings.es_indexes['persons']
    )

    headers = {'X-Not-Cache': 'True'}
    url = f"{test_settings.service_url}/api/v1/persons/{path_param['person_uuid']}"
    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert response['body'].get('full_name') == expected_answer.get('full_name')
    assert sorted(response['body'].get('role', [])) == sorted(expected_answer.get('role', []))
    assert sorted(response['body'].get('film_ids', [])) == sorted(expected_answer.get('film_ids', []))


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'query': 'Tony', 'sort': 'full_name.raw', 'page[size]': '50', 'page[number]': '1'},
            {'status': HTTPStatus.OK, 'length': 2, 'ids': ['0a3c2c6f-ef2d-4a38-a6e4-b8df0b6d9611', '7f22cd12-07b6-408e-aac1-ca75afb918c8']}
        ),
        (
            {'query': 'Tony', 'sort': 'id', 'page[size]': '1', 'page[number]': '2'},
            {'status': HTTPStatus.OK, 'length': 1, 'ids': ['7f22cd12-07b6-408e-aac1-ca75afb918c8']}
        ),
        (
            {'query': 'Tony', 'sort': '-id', 'page[size]': '1', 'page[number]': '2'},
            {'status': HTTPStatus.OK, 'length': 1, 'ids': ['0a3c2c6f-ef2d-4a38-a6e4-b8df0b6d9611']}
        ),
        (
            {'query': 'Fdourhggbsmk ssdfsdfdf ewewekkklwe', 'sort': '-id', 'page[size]': '50', 'page[number]': '1'},
            {'status': HTTPStatus.OK, 'length': 0, 'ids': []}
        )
    ]
)
async def test_search_person_pagination(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    """
    Поиск находит нужных персон, и только нужных.
    Поиск возвращает пустой список, если нет подходящих результатов.

    Пагинация на поиске работает
        размер и количество страниц корректное
    """
    await es_write_data(
        data=es_determination_data['persons'],
        es_index=test_settings.es_indexes['persons']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/persons/search'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)
    persons_ids = []
    if response['status'] == HTTPStatus.OK and type(response['body']) == list:
        persons_ids = [film['uuid'] for film in response['body']]

    assert response['status'] == expected_answer['status']
    assert len(persons_ids) == expected_answer['length']
    assert persons_ids == expected_answer['ids']
