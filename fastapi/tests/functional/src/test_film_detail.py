from http import HTTPStatus

import pytest

from functional.settings import test_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'path_param, expected_answer',
    [
        (
            {'film_uuid': '1a42b629-14af-4646-be32-16bd97d01e70'},
            {'status': HTTPStatus.OK,
                'title': 'Film heavy chair by development wikipedia amazon',
                'genre': [{'uuid': '9c91a5b2-eb70-4889-8581-ebe427370edd', 'name': 'Musical'}],
                'actors': [{'uuid': '3acaaf82-374a-4cc9-a039-7e67926146de', 'full_name': 'Robert Oneal'}, {'uuid': 'a8b56f85-346d-4b7e-80d3-d1af353e0c86', 'full_name': 'Teresa Martinez'}],
                'writers': [{'uuid': '3acaaf82-374a-4cc9-a039-7e67926146de', 'full_name': 'Robert Oneal'}, {'uuid': 'a8b56f85-346d-4b7e-80d3-d1af353e0c86', 'full_name': 'Teresa Martinez'}, {'uuid': '3b019fcb-f96d-4403-948c-93f3028d042b', 'full_name': 'Andrea Barry'}, {'uuid': '30c32323-c1b1-49c4-9f1f-f97c71cff814', 'full_name': 'Richard Jones'}],
                'directors': [{'uuid': '3acaaf82-374a-4cc9-a039-7e67926146de', 'full_name': 'Robert Oneal'}, {'uuid': 'a8b56f85-346d-4b7e-80d3-d1af353e0c86', 'full_name': 'Teresa Martinez'}, {'uuid': '8611f583-b2d1-4e3d-809e-2109c7867a38', 'full_name': 'Eric Wilson'}, {'uuid': '30c32323-c1b1-49c4-9f1f-f97c71cff814', 'full_name': 'Richard Jones'}],
            }
        ),
        (
            {'film_uuid': '50852f4f-0b09-4c41-b89a-28298a663359'},
            {'status': HTTPStatus.OK,
                'title': 'Hotel by year player',
                'genre': [{'uuid': 'ca88141b-a6b4-450d-bbc3-efa940e4953f', 'name': 'Mystery', }, {'uuid': 'f39d7b6d-aef2-40b1-aaf0-cf05e7048011', 'name': 'Horror', }, {'uuid': '9c91a5b2-eb70-4889-8581-ebe427370edd', 'name': 'Musical', }, {'uuid': '237fd1e4-c98e-454e-aa13-8a13fb7547b5', 'name': 'Romance', }, {'uuid': 'fb58fd7f-7afd-447f-b833-e51e45e2a778', 'name': 'Game-Show', }, {'uuid': '56b541ab-4d66-4021-8708-397762bff2d4', 'name': 'Music', }, {'uuid': 'e508c1c8-24c0-4136-80b4-340c4befb190', 'name': 'Reality-TV', }, {'uuid': 'f24fd632-b1a5-4273-a835-0119bd12f829', 'name': 'News', }],
                'actors': [],
                'writers': [{'uuid': '27f9e728-c618-4c1e-aa48-05421965e435', 'full_name': 'Amanda Griffin'}],
                'directors': [],
            }
        ),
        (
            {'film_uuid': '6480fdc0-f1c5-4f44-be08-3c1bcda6a326'},
            {'status': HTTPStatus.OK,
                'title': 'Morning explain light',
                'genre': [{'uuid': 'f39d7b6d-aef2-40b1-aaf0-cf05e7048011', 'name': 'Horror'}],
                'actors': [],
                'writers': [],
                'directors': [{'uuid': '8611f583-b2d1-4e3d-809e-2109c7867a38', 'full_name': 'Eric Wilson'}, {'uuid': '27f9e728-c618-4c1e-aa48-05421965e435', 'full_name': 'Amanda Griffin'}],
            }
        ),
        (
              {'film_uuid': '00af52ec-9345-4d66-adbe-50eb917f463a'},
              {'status': HTTPStatus.NOT_FOUND}
        )
    ]
)
async def test_film_detail(
          es_write_data,
          es_determination_data,
          path_param,
          expected_answer,
          aiohttp_get,
):
    """
    Получаем конкретный фильм по ID.
    У фильма корректный список genre.
    У фильма корректный список actors.
    У фильма корректный список directors.
    У фильма корректный список writers.
    У фильма корректный пустой список directors, когда у фильма нет directors.
    У фильма корректный пустой список actors, когда у фильма нет actors.
    У фильма корректный пустой список writers, когда у фильма нет writers.
    Получаем 404, когда передаем несуществующий ID.
    """
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = '{}/api/v1/films/{}'.format(
        test_settings.service_url, path_param['film_uuid'])
    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert response['body'].get('title') == expected_answer.get('title')
    assert response['body'].get('genre') == expected_answer.get('genre')
    assert response['body'].get('actors') == expected_answer.get('actors')
    assert response['body'].get('directors') == expected_answer.get('directors')
    assert response['body'].get('writers') == expected_answer.get('writers')
