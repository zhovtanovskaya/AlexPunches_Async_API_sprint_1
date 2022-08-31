
import datetime
import json
import uuid

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from functional.settings import test_settings

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором
#  `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'The Star'},
                {'status': 200, 'length': 60}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 60}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(
          es_write_data,
          es_clear_data,
          es_data,
          query_data,
          expected_answer,
):

    # 1. Генерируем данные для ES
    await es_write_data(es_data)

    # 3. Запрашиваем данные из ES по API

    headers = {'X-Not-Cache': 'True'}
    session = aiohttp.ClientSession(headers=headers)
    url = test_settings.service_url + '/api/v1/films/'

    async with session.get(url, params=query_data) as response:
        body = await response.json()  # noqa:F841
        headers = response.headers  # noqa:F841
        status = response.status
    await session.close()

    # 5. Очищаем данные
    await es_clear_data()

    # 4. Проверяем ответ

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']

