from functools import lru_cache

from pydantic import BaseSettings


class FrontendTogetherSettings(BaseSettings):
    websockets_host: str = 'localhost'
    websockets_port: int = 8000
    frontend_host: str = '0.0.0.0'
    frontend_port: int = 8000
    cloud_host: str
    cloud_port: int = 8000


@lru_cache()
def get_settings() -> FrontendTogetherSettings:
    """Получить синглтон конфигов."""
    return FrontendTogetherSettings()


config = get_settings()
