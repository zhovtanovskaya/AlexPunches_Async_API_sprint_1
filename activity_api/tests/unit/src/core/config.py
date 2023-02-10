import os
import sys

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))))
sys.path.append(BASE_DIR)


class MongoConn(BaseSettings):
    """Конфиг подключения к Монге."""

    mongo_user: str | None
    mongo_pw: str | None
    mongo_host: str | None
    mongo_rs: str | None
    mongo_auth_src_test: str
    test_mongo_url: str | None

    def get_conn(self) -> str:
        if self.test_mongo_url:
            return self.test_mongo_url
        uri = (
            'mongodb://{user}:{pw}@{host}/'
            '?replicaSet={rs}&authSource={auth_src}'
        )
        return uri.format(
            user=self.mongo_user,
            pw=self.mongo_pw,
            host=self.mongo_host,
            rs=self.mongo_rs,
            auth_src=self.mongo_auth_src_test,
        )


class TestSettings(BaseSettings):
    test_mongo_url: str = MongoConn().get_conn()
    mongo_tls_ca_file: str | None
    mongo_auth_src_test: str


settings = TestSettings()
