from enum import Enum
from functools import lru_cache
from typing import Type

from pydantic import BaseSettings, Field


class EventTypes(str, Enum):
    chat_message = 'chat_message'  # Сообщения в чат
    broadcast_command = 'broadcast_command'  # Команды на все плееры в руме (pause, play, ...)
    room_command = 'room_command'  # Команды WS-серверу (get_room_state, get_player_state, ...)
    chat_state = 'chat_state' # история всех сообщений чата для комнаты
    player_state = 'player_state' # состояние плеера (пока только timestamp, и статус "ведущий")


class PlayerStatuses(str, Enum):
    pause = 'pause'
    play = 'play'


class WebsocketSettings(BaseSettings):
    lead_role_name: str = 'lead'
    mute_role_name: str = 'mute'
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_db: int = 3
    event_types: Type[EventTypes] = EventTypes
    player_statuses: Type[PlayerStatuses] = PlayerStatuses


@lru_cache()
def get_settings() -> WebsocketSettings:
    """Получить синглтон конфигов."""
    return WebsocketSettings()


config = get_settings()
