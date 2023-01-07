"""Ассинхронный таймер."""
import functools
import time
from typing import Any, Callable

from config import logger


def async_timed():
    """Засечь, сколько времени будет выполняться функция."""
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                logger.info(f'finished in {total:.2f} second(s)')

        return wrapped
    return wrapper
