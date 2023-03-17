from functools import lru_cache

from pydantic import BaseSettings, Field


class WebsocketSettings(BaseSettings):
    lead_role_name: str = 'lead'
    mute_role_name: str = 'mute'
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    redis_db: int = 3


@lru_cache()
def get_settings() -> WebsocketSettings:
    """Получить синглтон конфигов."""
    return WebsocketSettings()


config = get_settings()
