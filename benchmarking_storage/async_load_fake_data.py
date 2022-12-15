import asyncio
from typing import Generator

import more_itertools
from aiochclient import ChClient
from aiohttp import ClientSession
from config import logger, settings

from utils.async_timer import async_timed
from utils.generator_fakes import generate_points

print(f'CHUNK_SIZE: {settings.chunk_size}')


async def load_data(client: ChClient, data: Generator):
    for points in more_itertools.ichunked(data, settings.chunk_size):
        await client.execute(
             'INSERT INTO '
             'shard.test (user_id, film_id, event_time, spawn_point) VALUES',
             *[(point.user_id, point.film_id, point.created_at, point.value)
                 for point in points]
        )


@async_timed()
async def run() -> None:
    data = generate_points(users_count=settings.fake_users_count,
                           films_count=settings.fake_films_count,
                           )
    async with ClientSession() as s:
        load_data_1 = asyncio.create_task(load_data(client=ChClient(s, url=f'http://{settings.ch_host}:8123'), data=data))
        load_data_2 = asyncio.create_task(load_data(client=ChClient(s, url=f'http://{settings.ch_host}:28123'), data=data))
        load_data_3 = asyncio.create_task(load_data(client=ChClient(s, url=f'http://{settings.ch_host}:38123'), data=data))

        await load_data_1
        await load_data_2
        await load_data_3


if __name__ == "__main__":
    asyncio.run(run())
