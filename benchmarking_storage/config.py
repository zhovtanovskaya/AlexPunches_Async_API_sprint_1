"""Конфиги."""
import logging

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Benchmarking')


class BaseConfig(BaseSettings):
    """Основной конфиаг."""

    ch_host: str = 'localhost'   # noqa
    # ch_host: str = '62.84.127.80'  # noqa
    ch_ports: list = ['9000', '9003', '9005']
    ch_port_1: str = '9000'  # TD. todo перевести на список во всех скриптах
    ch_port_2: str = '9003'
    ch_port_3: str = '9005'
    chunk_size: int = 10 ** 6

    fake_users_count: int = 10 ** 3
    fake_films_count: int = 10 ** 2

    cheker_interval: float = 3
    cheker_count: int = 11066000
    # cheker_count: int = 111168000

    vertica_connection_info = {
        'host': '127.0.0.1',
        'port': 5433,
        'user': 'dbadmin',
        'password': '',
        'database': 'docker',
        'autocommit': True,
    }


settings = BaseConfig()
