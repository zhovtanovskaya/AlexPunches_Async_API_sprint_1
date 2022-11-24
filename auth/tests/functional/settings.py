"""Конфиги для тестов."""

import logging
import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from functional.testdata.models import LoginHistory, Role, RoleUser, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__) + '/../../..')
load_dotenv(REPOSITORY_ROOT + '/.env.pytests')


class GetUrlMixin:
    """Микшен, чтобы создавать структуры данных."""

    host: str
    port: str

    def get_url(self):
        """Собирать урл из хоста и порта."""
        return f'http://{self.host}:{self.port}'


class RedisBaseUrl(BaseSettings, GetUrlMixin):
    """Переменные для Редиса."""

    host: str = Field('localhost', env='redis_host')
    port: str = Field('6379', env='redis_port')


class AuthBaseUrl(BaseSettings, GetUrlMixin):
    """Хост приложения."""

    host: str = Field('localhost', env='auth_host')
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

    # TODO придумать модель данных покрасивее
    users_tablename = 'users'
    roles_tablename = 'roles'
    roles_users_tablename = 'roles_users'
    login_histories_tablename = 'login_history'
    login_histories_tablename_smart = 'login_history_smart'
    login_histories_tablename_web = 'login_history_web'
    login_histories_tablename_mobile = 'login_history_mobile'
    fake_data_map = {
        users_tablename: User,
        roles_tablename: Role,
        roles_users_tablename: RoleUser,
        login_histories_tablename: LoginHistory,
    }

    # TODO сделать при помощи urllib3
    api_version_url: str = '/api/v1'
    signin_endpoint: str = service_url + api_version_url + '/signin'
    signup_endpoint: str = service_url + api_version_url + '/signup'
    signout_endpoint: str = service_url + api_version_url + '/signout'
    refresh_endpoint: str = service_url + api_version_url + '/refresh'
    users_endpoint: str = api_version_url + '/users'
    roles_endpoint: str = api_version_url + '/roles'
    login_histories_endpoint: str = api_version_url + '/login_histories'
    profile_endpoint: str = api_version_url + '/profile'


test_settings = TestSettings()
