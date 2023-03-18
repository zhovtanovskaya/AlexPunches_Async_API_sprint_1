from enum import Enum
from functools import lru_cache
from typing import Type

from pydantic import BaseSettings, Field


class EventTypes(str, Enum):
    chat_message = 'chat_message'
    player_command = 'player_command'
    room_state = 'room_state'


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
