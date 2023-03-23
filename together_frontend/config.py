from functools import lru_cache

from pydantic import BaseSettings


class FrontendTogetherSettings(BaseSettings):
    websockets_host: str = 'localhost'
    websockets_port: int = 8000
    frontend_host: str
    frontend_port: int


@lru_cache()
def get_settings() -> FrontendTogetherSettings:
    """Получить синглтон конфигов."""
    return FrontendTogetherSettings()


config = get_settings()
