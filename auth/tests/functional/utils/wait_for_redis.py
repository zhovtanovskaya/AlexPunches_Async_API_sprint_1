"""Дождаться готовности хоста с Редисом."""

import os
import sys

from redis import Redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from functional.settings import logger, test_settings  # noqa
from functional.utils.backoff import backoff  # noqa


class RedisPingError(Exception):
    """Exception недоступности Редиса."""

    ...


@backoff(RedisPingError, logger=logger)
def ping_redis(redis_client):
    """Пинговать Редис пока не ответит."""
    if not redis_client.ping():
        raise RedisPingError()
    redis_client.close()


if __name__ == '__main__':
    _redis_client = Redis(test_settings.redis_host, test_settings.redis_port)

    ping_redis(redis_client=_redis_client)
