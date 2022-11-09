"""Все конфиги для Auth-приложения."""

import logging
import os
from datetime import timedelta
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, PostgresDsn

from core.db import db
from core.logger import LOGGING
from models import Role, User

REPOSITORY_ROOT = os.path.abspath(os.path.dirname(__file__) + '/../../..')
load_dotenv(REPOSITORY_ROOT + '/.env.dev')
logging_config.dictConfig(LOGGING)


class PgBaseUrl(BaseSettings):
    """Настройки подкдючения к постгрессу."""

    scheme: str = 'postgresql'
    username: str = Field(..., env='postgres_user_auth')
    password: str = Field(..., env='postgres_password_auth')
    host: str = Field('localhost', env='db_host_auth')
    port: str = Field('5432', env='db_port_auth')
    database_name: str = Field(..., env='postgres_db_auth')

    def get_url(self):
        """Метод для удобной конкатинации настроек в одну строку."""
        return (
            f'{self.scheme}://{self.username}:{self.password}@'
            f'{self.host}:{self.port}/{self.database_name}'
        )


class FlaskConfig(BaseSettings):
    """Настройки Фласка."""

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PgBaseUrl().get_url()
    SECRET_KEY: str = Field(..., env='flask_secret_key')
    WTF_CSRF_ENABLED: bool = False
    SECURITY_PASSWORD_HASH: str = 'bcrypt'
    SECURITY_PASSWORD_SALT: str = Field(..., env='security_password_salt')
    SECURITY_SEND_REGISTER_EMAIL: bool = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL: bool = False
    SECURITY_SEND_PASSWORD_RESET_EMAIL: bool = False
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL: bool = False
    JWT_SECRET_KEY: str = Field(..., min_length=8)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta
    JWT_REFRESH_TOKEN_EXPIRES: timedelta


class ApiSettings(BaseSettings):
    """Настройки сервиса Auth."""

    project_name: str = Field('Movies', env='project_name')

    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_minsize: int = 10
    redis_maxsize: int = 20
    redis_expire_in_seconds: int = 60 * 5

    flask_config: FlaskConfig = FlaskConfig()
    paginator_per_page: int = 20
    paginator_start_page: int = 1

    user_model: db.Model = User
    role_model: db.Model = Role
    admin_role_name: str = 'admin'


@lru_cache()
def get_settings() -> ApiSettings:
    """Создать и/или вернуть синглтон для конфигов."""
    return ApiSettings()


config = get_settings()

logger = logging.getLogger(config.project_name)
