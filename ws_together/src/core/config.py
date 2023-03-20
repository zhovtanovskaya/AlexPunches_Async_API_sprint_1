import logging
from enum import Enum
from functools import lru_cache
from logging import config as logging_config
from typing import Type

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class EventTypes(str, Enum):
    broadcast_message = 'broadcast_message'  # Сообщения в чат
    broadcast_command = 'broadcast_command'  # Команды на все плееры в руме (pause, play, ...)
    room_request = 'room_request'  # Запросы WS-серверу (get_room_state, get_player_state, ...)
    chat_state = 'chat_state' # история всех сообщений чата для комнаты
    player_state = 'player_state' # состояние плеера (пока только timestamp, и статус "ведущий")
    error = 'error' # Сообщение об ошибке (для клиента)


class PlayerStatuses(str, Enum):
    pause = 'pause'
    play = 'play'


class RoomRequests(str, Enum):
    get_room_state = 'get_room_state'
    get_player_state = 'get_player_state'
    set_state = 'set_state'


class WebsocketSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    lead_role_name: str = 'lead'
    mute_role_name: str = 'mute'
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_db: int = 3
    event_types: Type[EventTypes] = EventTypes
    player_statuses: Type[PlayerStatuses] = PlayerStatuses
    room_requests: Type[RoomRequests] = RoomRequests


@lru_cache()
def get_settings() -> WebsocketSettings:
    """Получить синглтон конфигов."""
    return WebsocketSettings()


config = get_settings()
logger = logging.getLogger(config.project_name)
