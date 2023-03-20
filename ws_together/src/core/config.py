import logging
from enum import Enum
from functools import lru_cache
from logging import config as logging_config
from typing import Type

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class EventTypes(str, Enum):
    # Сообщения в чат
    broadcast_message = 'broadcast_message'
    # Команды на все плееры в руме (pause, play, ...)
    broadcast_command = 'broadcast_command'
    # Запросы WS-серверу (get_room_state, get_player_state, ...)
    room_request = 'room_request'
    # история всех сообщений чата для комнаты
    chat_state = 'chat_state'
    # состояние плеера (timestamp, и статус "ведущий")
    player_state = 'player_state'
    # Сообщение об ошибке (для клиента)
    error = 'error'


class PlayerStatuses(str, Enum):
    pause = 'pause'
    play = 'play'
    stop = 'stop'


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
