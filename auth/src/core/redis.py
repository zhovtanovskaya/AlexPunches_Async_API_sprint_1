"""Подключение к Redis для хранения JWT."""

import redis

from core.config import config

jwt_redis_blocklist = redis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    db=0,
    decode_responses=True,
)
