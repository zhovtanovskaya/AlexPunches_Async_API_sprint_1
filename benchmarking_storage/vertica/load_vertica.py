"""Загрузка данных в вертику."""
import os
import sys
from typing import Generator

import more_itertools
import vertica_python

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
sys.path.append(BASE_DIR)

from config import settings

from utils.generator_fakes import generate_points
from utils.timer import timed


@timed
def load_data(data: Generator):
    """Загрузить данные в Вертику."""
    with vertica_python.connect(**settings.vertica_connection_info) as conn:
        cursor = conn.cursor()
        for points in more_itertools.ichunked(data, settings.chunk_size):

            cursor.executemany(
                 'INSERT INTO views(user_id, film_id, event_time, spawn_point)'
                 ' VALUES (%s, %s, %s, %s)',
                 [(point.user_id, point.film_id, point.created_at, point.value)
                     for point in points],
             )


def run() -> None:
    """Запуск."""
    data = generate_points(users_count=settings.fake_users_count,
                           films_count=settings.fake_films_count,
                           )
    load_data(data)


if __name__ == '__main__':
    run()
