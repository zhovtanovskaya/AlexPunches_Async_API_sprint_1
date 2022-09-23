"""
/api/v1/persons/<uuid:UUID>/film
Получаем все фильмы, в которых есть персона. По ID персоны.

/api/v1/persons/search?query=captain&page[number]=1&page[size]=50
Поиск находит нужных персон, и только нужных.
Поиск возвращает пустой список, если нет подходящих результатов.

Пагинация на поиске работает
    размер и количество страниц корректное
"""

import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'path_param, expected_answer',
    [
        (
            {'person_uuid': '6c0be55c-90e6-49e1-a44f-c3a96d0c62c3'},
            {'status': 200,
                'full_name': 'Taylor Perry',
                'role': ['directors', 'actors', 'writers'],
                'film_ids': ['f0fcccc6-fb46-4d39-8772-c3475cba9be3', 'fdc12930-82ae-452f-ad40-76bcf9cb2ee8', '0b36f3cd-0acf-4ba4-8410-30ae56525ce0', 'e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
            {'person_uuid': '7f22cd12-07b6-408e-aac1-ca75afb918c8'},
            {'status': 200,
                'full_name': 'Tonya Sharp',
                'role': ['actors'],
                'film_ids': ['e32866d3-0d6a-48b0-beda-9ab9bec60ffe'],
            }
        ),
        (
              {'person_uuid': '01af52ec-9345-4d66-adbe-50e54577434e'},
              {'status': 404}
        )
    ]
)
@pytest.mark.asyncio
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
    url = f"{test_settings.service_url}/api/v1/persons/{path_param['person_uuid']}/"
    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert response['body'].get('full_name') == expected_answer.get('full_name')
    assert response['body'].get('role', []).sort() == expected_answer.get('role', []).sort()
    assert response['body'].get('film_ids', []).sort() == expected_answer.get('film_ids', []).sort()
