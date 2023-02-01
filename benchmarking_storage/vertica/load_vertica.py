"""Загрузка данных в вертику."""
from typing import Generator

import more_itertools
import vertica_python

from config import settings
from utils.generator_fakes import generate_points
from utils.timer import timed


@timed
def load_data(chunk_size: int, data: Generator):
    """Загрузить данные в Вертику."""
    with vertica_python.connect(**settings.vertica_connection_info) as conn:
        cursor = conn.cursor()
        for points in more_itertools.ichunked(data, chunk_size):

            cursor.executemany(
                 'INSERT INTO views(user_id, film_id, event_time, spawn_point)'
                 ' VALUES (%s, %s, %s, %s)',
                 [(point.user_id, point.film_id, point.created_at, point.value)
                     for point in points],
             )


def run(users_count: int, films_count: int, chunk_size: int) -> None:
    """Запуск."""
    data = generate_points(users_count, films_count)
    load_data(chunk_size, data)
