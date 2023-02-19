import logging
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AmqpConect(BaseSettings):
    notifications_queue_user: str = 'user'
    notifications_queue_password: str = '123456'
    notifications_queue_host: str = '51.250.2.205'
    notifications_queue_port: str = '5672'

    def get_conn(self) -> str:
        """Получить троку подключения к Реббиту."""
        return str(
            f'amqp://{self.notifications_queue_user}'
            f':{self.notifications_queue_password}@'
            f'{self.notifications_queue_host}:{self.notifications_queue_port}/'
        )


class WorkerSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    queue_name: str = 'notifications'
    queue_conn: str = AmqpConect().get_conn()
    def_priority: int = 5
    def_timezone: str = 'Europe/Moscow'
    night_start_hour: int = Field(22, ge=0, le=24)
    night_stop_hour: int = Field(8, ge=0, le=24)

    mapping_senders_type: dict = {
        'smart_email': ''
    }


@lru_cache()
def get_settings() -> WorkerSettings:
    """Получить синглтон конфигов."""
    return WorkerSettings()


config = get_settings()
logger = logging.getLogger(config.project_name)
