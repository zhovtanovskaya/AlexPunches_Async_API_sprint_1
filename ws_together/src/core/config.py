from functools import lru_cache

from pydantic import BaseSettings, Field


class WebsocketSettings(BaseSettings):
    pass


@lru_cache()
def get_settings() -> WebsocketSettings:
    """Получить синглтон конфигов."""
    return WebsocketSettings()
