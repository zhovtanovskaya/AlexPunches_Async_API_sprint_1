"""Таймер."""
import functools
import time
import tracemalloc
import typing

from config import logger


def timed(func: typing.Callable) -> typing.Callable:
    """Засечь, сколько времени будет выполняться функция."""
    @functools.wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        tracemalloc.start()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = (time.time() - start) * 1000
        _, mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logger.info(f'{func.__name__}:\n    '
                    f'max_memory: {mem_peak/1000_000:,.3f} mb\n    '
                    f'exec time: {elapsed_time:,.3f} ms',
                    )

        return result
    return wrapper
