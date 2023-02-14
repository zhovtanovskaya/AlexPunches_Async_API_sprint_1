import logging
import os
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class GetUrlMixin:
    scheme: str = 'http'
    host: str
    port: str

    def get_url(self):
        return f'{self.scheme}://{self.host}:{self.port}'


class EsBaseUrl(BaseSettings, GetUrlMixin):
    host: str = Field(..., env='es_host')
    port: str = Field('9200', env='es_port')


class EsIndex(BaseSettings):
    name: str
    search_field: str | None = None
    id_field: str = 'id'


class ApiSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    use_cache: bool = Field(True, env='use_cache')

    # Настройки JWT-авторизации для путей API,
    # которые должны быть доступны только аутентифицированным
    # пользователям с указанными ролями.
    jwt_secret_key: str = Field('')
    jwt_algorithm: str = 'HS256'

    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_minsize: int = 10
    redis_maxsize: int = 20
    redis_cache_expire_in_seconds: int = 60 * 5

    elastic_url: str = EsBaseUrl().get_url()
    elastic_host: str = EsBaseUrl().host
    elastic_port: str = EsBaseUrl().port
    elastic_keep_alive: str = '1m'
    elastic_default_sort: str = 'id'

    es_indexes: dict = {
        'movies': EsIndex(name='movies', search_field='title'),
        'genres': EsIndex(name='genres', search_field='name'),
        'persons': EsIndex(name='persons', search_field='name'),
    }

    api_port: str = '8000'
    api_sentry_dsn: str = ''


@lru_cache()
def get_settings() -> ApiSettings:
    return ApiSettings()


config = get_settings()

logger = logging.getLogger(config.project_name)
