"""Конфиги."""
import logging
from urllib.parse import quote_plus as quote

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Benchmarking')


class MongoConn(BaseSettings):
    """Конфиг подключения к Монге."""

    mongo_user: str
    mongo_pw: str
    mongo_host: str
    mongo_rs: str
    mongo_auth_src: str

    def get_conn(self) -> str:
        return 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(  # noqa
            user=quote(self.mongo_user),
            pw=quote(self.mongo_pw),
            hosts=','.join([self.mongo_host]),
            rs=self.mongo_rs,
            auth_src=self.mongo_auth_src,
        )


class BaseConfig(BaseSettings):
    """Основной конфиаг."""

    ch_host: str = 'localhost'   # noqa
    # ch_host: str = '158.160.54.14'  # noqa
    ch_ports: list = ['9000', '9003', '9005']
    chunk_size: int = 10 ** 5

    fake_users_count: int = 10 ** 2
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

    mongo_conn = MongoConn().get_conn()
    mongo_tls_ca_file: str


settings = BaseConfig()
