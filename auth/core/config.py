import logging
from functools import lru_cache
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class GetUrlMixin:
    scheme: str
    username: str
    password: str
    host: str
    port: str
    database_name: str

    def get_url(self):
        return (
            f'{self.scheme}://{self.username}:{self.password}@'
            f'{self.host}:{self.port}/{self.database_name}'
        )


class PgBaseUrl(BaseSettings, GetUrlMixin):
    scheme: str = 'postgresql'
    username: str = Field(..., env='postgres_user_auth')
    password: str = Field(..., env='postgres_password_auth')
    host: str = Field('localhost', env='db_host_auth')
    port: str = Field('5432', env='db_port_auth')
    database_name: str = Field(..., env='postgres_db_auth')


class ApiSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')

    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_minsize: int = 10
    redis_maxsize: int = 20
    redis_cache_expire_in_seconds: int = 60 * 5

    db_url: str = PgBaseUrl().get_url()


@lru_cache()
def get_settings() -> ApiSettings:
    return ApiSettings()


config = get_settings()

logger = logging.getLogger(config.project_name)
