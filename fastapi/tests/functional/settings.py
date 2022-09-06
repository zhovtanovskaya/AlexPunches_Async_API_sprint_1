from functional.testdata import es_mapping, es_setting
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


class EsIndex(BaseSettings):
    name: str
    mapping: dict
    id_field: str = 'id'
    setting: dict = es_setting.es_setting


class TestSettings(BaseSettings):
    es_url: str = EsBaseUrl().get_url()
    redis_host: str = RedisBaseUrl().host
    redis_port: str = RedisBaseUrl().port

    redis_url: str = RedisBaseUrl().get_url()
    service_url: str = ApiBaseUrl().get_url()

    es_indexes: dict = {
        'movies': EsIndex(name='movies', mapping=es_mapping.movie_mappings),
        'genres': EsIndex(name='genres', mapping=es_mapping.genre_mapping),
        'persons': EsIndex(name='persons', mapping=es_mapping.person_mapping),
    }


test_settings = TestSettings()
