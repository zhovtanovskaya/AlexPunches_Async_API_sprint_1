"""Backoff для определенных exceptions."""
import asyncio
from functools import wraps

from core.config import logger
from utils import messages as msg


def backoff(
          *exceptions,
          _logger: logger,
          start_sleep_time: float = 0.1,
          factor: int = 2,
          border_sleep_time: int = 30,
):
    """Функция для повторного выполнения функции через некоторое время."""
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    _logger.warning(msg.i_will_try_again,
                                    sleep_time)
                    await asyncio.sleep(sleep_time)
                    if sleep_time < border_sleep_time:
                        sleep_time *= factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper
