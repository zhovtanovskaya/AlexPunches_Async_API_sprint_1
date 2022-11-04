"""Конфиги для тестов."""

import logging

from pydantic import BaseSettings, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetUrlMixin:
    """Микшен, чтобы создавать структуры данных."""

    host: str
    port: str

    def get_url(self):
        """Собирать урл из хоста и порта."""
        return f'http://{self.host}:{self.port}'


class RedisBaseUrl(BaseSettings, GetUrlMixin):
    """Переменные для Редиса."""

    host: str = Field(..., env='redis_host')
    port: str = Field('6379', env='redis_port')


class AuthBaseUrl(BaseSettings, GetUrlMixin):
    """Хост приложения."""

    host: str = Field(..., env='auth_host')
    port: str = Field('5000', env='auth_port')


class PgBaseUrl(BaseSettings):
    """Переменные для подключения к Постгрессу."""

    scheme: str = 'postgresql'
    username: str = Field(..., env='postgres_user_auth')
    password: str = Field(..., env='postgres_password_auth')
    host: str = Field(..., env='db_host_auth')
    port: str = Field('5432', env='db_port_auth')
    db_name: str = Field(..., env='postgres_db_auth')

    def get_url(self):
        """Собирать урл из параметров."""
        return f'{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}'  # noqa


class TestSettings(BaseSettings):
    """Класс с конфигами для тестов."""

    redis_host: str = RedisBaseUrl().host
    redis_port: str = RedisBaseUrl().port

    redis_url: str = RedisBaseUrl().get_url()
    service_url: str = AuthBaseUrl().get_url()

    pg_settings: PgBaseUrl = PgBaseUrl()

    users_tablename = 'users'
    roles_tablename = 'roles'
    roles_users_tablename = 'roles_users'


test_settings = TestSettings()
