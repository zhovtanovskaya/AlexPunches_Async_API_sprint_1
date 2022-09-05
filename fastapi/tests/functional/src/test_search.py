import pytest
from functional.settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'search': 'Question set'}, {'status': 200, 'length': 1}),
        ({'search': 'Glass'}, {'status': 200, 'length': 2})
    ]
)
# @pytest.mark.skipif(True, reason="Api not ready")
@pytest.mark.asyncio
async def test_search(
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
    url = test_settings.service_url + '/api/v1/films/search/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
