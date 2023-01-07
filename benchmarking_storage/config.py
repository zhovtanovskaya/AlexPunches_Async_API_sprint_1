"""Конфиги."""
import logging

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Benchmarking')


class BaseConfig(BaseSettings):
    """Основной конфиаг."""

    ch_host: str = 'localhost'   # noqa
    # ch_host: str = '158.160.54.14'  # noqa
    ch_ports: list = ['9000', '9003', '9005']
    chunk_size: int = 10 ** 3

    fake_users_count: int = 10 ** 3
    fake_films_count: int = 10 ** 3

    cheker_interval: float = 15
    # cheker_count: int = 11066000  # noqa
    cheker_count: int = 111168000

    vertica_connection_info = {
        'host': '127.0.0.1',
        'port': 5433,
        'user': 'dbadmin',
        'password': '',
        'database': 'docker',
        'autocommit': True,
    }


settings = BaseConfig()
