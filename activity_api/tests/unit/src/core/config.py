from urllib.parse import quote_plus as quote

from pydantic import BaseSettings


class MongoConn(BaseSettings):
    """Конфиг подключения к Монге."""

    mongo_user: str
    mongo_pw: str
    mongo_host: str
    mongo_rs: str
    test_mongo_auth_src: str
    test_mongo_url: str

    def get_conn(self) -> str:
        if self.test_mongo_url:
            return self.test_mongo_url
        uri = (
            'mongodb://{user}:{pw}@{host}/'
            '?replicaSet={rs}&authSource={auth_src}'
            '&retryWrites=true&w=majority'
        )
        return uri.format(
            user=quote(self.mongo_user),
            pw=quote(self.mongo_pw),
            host=self.mongo_host,
            rs=self.mongo_rs,
            auth_src=self.test_mongo_auth_src,
        )


class TestSettings(BaseSettings):
    test_mongo_url: str = MongoConn().get_conn()
    mongo_tls_ca_file: str | None
    test_mongo_auth_src: str


settings = TestSettings()
