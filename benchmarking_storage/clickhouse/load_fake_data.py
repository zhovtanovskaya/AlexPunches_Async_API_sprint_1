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
from typing import Generator

import more_itertools
from clickhouse_driver import Client

from config import logger, settings
from utils.generator_fakes import generate_points
from utils.timer import timed


@timed
def load_data(chunk_size: int, data: Generator):
    """Загрузить данные в кликхаус на первый шард."""
    for points in more_itertools.ichunked(data, chunk_size):
        client = Client(host=settings.ch_host, port=settings.ch_ports[0])
        client.execute(
             'INSERT INTO '
             'shard.test (user_id, film_id, event_time, spawn_point) VALUES',
             ((point.user_id, point.film_id, point.created_at, point.value)
                 for point in points),
         )


def run(users_count: int, films_count: int, chunk_size: int) -> None:
    """Запуск."""
    logger.info(f'chunk_size: {chunk_size}')
    load_data(chunk_size, generate_points(users_count, films_count))
