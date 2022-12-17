"""Ассинхронное добавление жанных на разные шарды."""
import asyncio
from typing import Any, Generator

import more_itertools
from asynch import connect
from asynch.cursors import DictCursor
from config import logger, settings

from utils.async_timer import async_timed
from utils.generator_fakes import generate_points

logger.info(f'chunk_size: {settings.chunk_size}')


async def load_data(connection: Any, data: Generator):
    """Загрузить данные в Кликхаус."""
    timer = 0
    count_insert = 0
    async with connection.cursor(cursor=DictCursor) as cursor:
        for points in more_itertools.ichunked(data, settings.chunk_size):
            await cursor.execute(
                 'INSERT INTO '
                 'shard.test (user_id, film_id, event_time, spawn_point) VALUES', # noqa
                 [(point.user_id, point.film_id, point.created_at, point.value)
                     for point in points],
            )
            timer += cursor.connection._connection.last_query.elapsed
            count_insert += 1
    logger.info(f'{connection.port}: {count_insert}, {timer:.3f}')


@async_timed()
async def run() -> None:
    """Запуск."""
    data = generate_points(users_count=settings.fake_users_count,
                           films_count=settings.fake_films_count,
                           )
    tasks = [
        load_data(connection=await connect(host=settings.ch_host, port=port),
                  data=data)
        for port in settings.ch_ports
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(run())
