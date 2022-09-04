from pydantic import BaseSettings, Field


class GetUrlMixin:
    host: str
    port: str

    def get_url(self):
        return 'http://{}:{}'.format(self.host, self.port)


class EsBaseUrl(BaseSettings, GetUrlMixin):
    host: str = Field(..., env='es_host')
    port: str = Field('9200', env='es_port')


class RedisBaseUrl(BaseSettings, GetUrlMixin):
    host: str = Field(..., env='redis_host')
    port: str = Field('6379', env='redis_port')


class ApiBaseUrl(BaseSettings, GetUrlMixin):
    host: str = Field(..., env='api_host')
    port: str = Field('8000', env='api_port')


class TestSettings(BaseSettings):
    es_host: str = EsBaseUrl().get_url()
    es_index: str = 'movies'
    es_id_field: str = 'id'
    # es_index_mapping: dict = ''
    redis_host: str = RedisBaseUrl().host
    redis_port: str = RedisBaseUrl().port

    redis_url: str = RedisBaseUrl().get_url()
    service_url: str = ApiBaseUrl().get_url()


test_settings = TestSettings()
