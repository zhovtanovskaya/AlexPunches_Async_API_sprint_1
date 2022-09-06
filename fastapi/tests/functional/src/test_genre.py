import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'expected_answer',
    [
        {'status': 200, 'length': 100, 'type_body': list}
    ]
)
@pytest.mark.asyncio
async def test_genres_list(
          es_write_data,
          es_fake_data_fix_count,
          expected_answer,
          aiohttp_get,
):
    """Получаем все жанры."""
    await es_write_data(
        data=es_fake_data_fix_count['genres'],
        es_index=test_settings.es_indexes['genres']
    )
    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/genres/'

    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert type(response['body']) == expected_answer['type_body']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'expected_answer',
    [
        {'status': 200, 'length': 0, 'type_body': list}
    ]
)
@pytest.mark.asyncio
async def test_genres_empty_list(
          es_write_data,
          expected_answer,
          aiohttp_get,
):
    """Получаем пустой список, когда нет жанров."""
    await es_write_data(
        data=None,
        es_index=test_settings.es_indexes['genres']
    )
    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/genres/'

    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert type(response['body']) == expected_answer['type_body']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'path_param, expected_answer',
    [
        (
            {'genre_uuid': 'fb58fd7f-7afd-447f-b833-e51e45e2a778'},
            {'status': 200,
                'name': 'Game-Show',
                'description': 'Have heart cover analysis carry specific media husband.',
            }
        ),
        (
            {'genre_uuid': 'f24fd632-b1a5-4273-a835-0119bd12f829'},
            {'status': 200,
                'name': 'News',
                'description': None,
            }
        ),
        (
              {'genre_uuid': '01af52ec-9345-4d66-adbe-50eb917f463e'},
              {'status': 404}
        )
    ]
)
@pytest.mark.asyncio
async def test_genre_detail(
          es_write_data,
          es_determination_data,
          path_param,
          expected_answer,
          aiohttp_get,
):
    """
    Получаем конкретный жанр по ID.
    У жанра корректный name.
    У жанра корректный description.
    У фильма корректный пустой description, когда у жанра нет description.
    Получаем 404, когда передаем несуществующий ID.
    """
    await es_write_data(
        data=es_determination_data['genres'],
        es_index=test_settings.es_indexes['genres']
    )

    headers = {'X-Not-Cache': 'True'}
    url = '{}/api/v1/genres/{}/'.format(
        test_settings.service_url, path_param['genre_uuid'])
    response = await aiohttp_get(url=url, headers=headers)

    assert response['status'] == expected_answer['status']
    assert response['body'].get('name') == expected_answer.get('name')
    assert response['body'].get('description') == expected_answer.get('description')
