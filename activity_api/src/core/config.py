"""Конфиги приложения."""
import logging
import os
from functools import lru_cache
from logging import config as logging_config
from typing import Optional
from urllib.parse import quote_plus as quote

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class MongoConn(BaseSettings):
    """Конфиг подключения к Монге."""

    mongo_user: str
    mongo_pw: str
    mongo_host: str
    mongo_rs: str
    mongo_auth_src: str

    def get_conn(self) -> str:
        return 'mongodb://{user}:{pw}@{host}/?replicaSet={rs}&authSource={auth_src}&retryWrites=true&w=majority'.format(  # noqa
            user=quote(self.mongo_user),
            pw=quote(self.mongo_pw),
            host=self.mongo_host,
            rs=self.mongo_rs,
            auth_src=self.mongo_auth_src,
        )


class ApiSettings(BaseSettings):
    """Класс с основными конфигими."""

    project_name: str = Field('Movies', env='project_name')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Настройки JWT-авторизации для путей API,
    # которые должны быть доступны только аутентифицированным
    # пользователям с указанными ролями.
    jwt_secret_key: str = Field('')
    jwt_algorithm: str = 'HS256'

    activity_api_port: str = '8000'

    event_store_host: str = 'localhost'
    event_store_port: str = '9092'
    film_progress_topic: str = 'views'
    activity_sentry_dsn: Optional[str]
    # mongo_url: str = ''
    mongo_url: str = MongoConn().get_conn()
    mongo_tls_ca_file: Optional[str]


@lru_cache()
def get_settings() -> ApiSettings:
    """Получить синглтон конфигов."""
    return ApiSettings()


config = get_settings()

logger = logging.getLogger(config.project_name)
