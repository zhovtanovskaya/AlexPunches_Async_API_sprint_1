from abc import ABC
from functools import lru_cache
from typing import Optional
import aioredis
# from aioredis import Redis
from db.redis import redis
from models.film import Film

from fastapi import Depends
from core import config


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class RedisClient:
    def __init__(self):
        self.redis = redis

    async def __call__(self):
        pass

    async def get_raw_by_key(self, key: str) -> str:
        return await self.redis.get(key)

    async def put_rqw_to_cache(self, key: str, raw_data) -> None:
        await self.redis.set(key, raw_data, expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_redis_service(
          redis: RedisClient = RedisClient()
) -> RedisClient:
    return redis
