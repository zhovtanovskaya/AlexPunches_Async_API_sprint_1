"""Сервис сокращения ссылок."""
from functools import lru_cache

from core.config import config
from db.redis import shortlink_redis as redis
from utils.random_generator import random_string


class ShortlinkService:
    """Сервис для работы с сокращателем ссылок."""

    def create_shortlink(
        self,
        longlink: str,
        days_ttl: int = config.shortlink_ttl
    ) -> str:
        """Создать короткую ссылку для длинной."""
        shortlink_id = random_string(config.shortlink_length)
        shortlink = redis.setnx(name=shortlink_id, value=longlink)
        if not shortlink:
            self.create_shortlink(longlink=longlink, days_ttl=days_ttl)
        redis.getex(name=shortlink_id, ex=days_ttl * 60 * 60 * 24)

        return f'/{config.shortlink_prefix}/{shortlink_id}'

    @staticmethod
    def get_longlink_by_shortlink_id(link_id: str) -> str:
        """Вернуть длинную ссылку по ИД короткой."""
        return redis.get(link_id)


@lru_cache()
def get_shortlink_service() -> ShortlinkService:
    """Создать и/или вернуть синглтон ShortlinkService."""
    return ShortlinkService()
