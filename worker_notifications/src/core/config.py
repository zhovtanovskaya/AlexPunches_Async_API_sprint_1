import logging
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AmqpConect(BaseSettings):
    queue_user: str = 'user'
    queue_password: str = '123456'
    queue_host: str = '158.160.55.33'
    queue_port: str = '5672'

    def get_conn(self):
        return f'amqp://{self.queue_user}:{self.queue_password}@{self.queue_host}:{self.queue_port}/'


class WorkerSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    queue_name: str = 'notifications'
    queue_conn: str = AmqpConect().get_conn()


@lru_cache()
def get_settings() -> WorkerSettings:
    """Получить синглтон конфигов."""
    return WorkerSettings()


config = get_settings()
logger = logging.getLogger(config.project_name)
