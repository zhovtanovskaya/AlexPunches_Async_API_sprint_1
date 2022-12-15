"""Бенчмаркинг кликхауса.

Тачка:
Платформа Intel Ice Lake
Гарантированная доля vCPU 100%
vCPU 4
RAM 16 ГБ
Объём дискового пространства 100 ГБ
Прерываемая да

Все 3 шарда в докерах на одной машине.
"""
import random
from typing import Generator

import more_itertools
from clickhouse_driver import Client
from config import logger, settings

from utils.generator_fakes import generate_points
from utils.timer import timed

logger.info(f'chunk_size: {settings.chunk_size}')


@timed
def load_data(data: Generator):
    """Загрузить данные в кликхаус.

    Каждая пачка на случайный шард.
    """
    clients = (
        Client(host=settings.ch_host, port=settings.ch_port_1),
        Client(host=settings.ch_host, port=settings.ch_port_2),
        Client(host=settings.ch_host, port=settings.ch_port_3),
    )
    for points in more_itertools.ichunked(data, settings.chunk_size):
        client = random.choice(clients)
        client.execute(
             'INSERT INTO '
             'shard.test (user_id, film_id, event_time, spawn_point) VALUES',
             ((point.user_id, point.film_id, point.created_at, point.value)
                 for point in points),
         )


def run() -> None:
    data = generate_points(users_count=settings.fake_users_count,
                           films_count=settings.fake_films_count,
                           )
    load_data(data)


if __name__ == "__main__":
    run()
