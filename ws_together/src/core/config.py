import logging
from functools import lru_cache
from logging import config as logging_config
from typing import Type

from pydantic import BaseSettings, Field

from core.logger import LOGGING
from services.models.enums import EventTypes, PlayerStatuses, RoomRequests

logging_config.dictConfig(LOGGING)


class WebsocketSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    lead_role_name: str = 'lead'
    mute_role_name: str = 'mute'
    admin_role_name: str = 'admin'
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_db: int = 3
    event_types: Type[EventTypes] = EventTypes
    player_statuses: Type[PlayerStatuses] = PlayerStatuses
    room_requests: Type[RoomRequests] = RoomRequests
    chat_bot_name: str = 'Bot'
    jwt_secret_key: str = Field('jwt_secret_key')
    jwt_algorithm: str = 'HS256'


@lru_cache()
def get_settings() -> WebsocketSettings:
    """Получить синглтон конфигов."""
    return WebsocketSettings()


config = get_settings()
logger = logging.getLogger(config.project_name)
