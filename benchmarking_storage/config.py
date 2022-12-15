import logging

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Benchmarking')


class BaseConfig(BaseSettings):
    ch_host: str = 'localhost'
    ch_ports: list = ['9000', '9003', '9005']
    ch_port_1: str = '9000'
    ch_port_2: str = '9003'
    ch_port_3: str = '9005'
    chunk_size: int = 10 ** 5

    fake_users_count: int = 1000
    fake_films_count: int = 1000

    cheker_interval: float = 10
    cheker_count: int = 111168000


settings = BaseConfig()
