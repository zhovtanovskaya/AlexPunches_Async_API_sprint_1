from functools import wraps
from logging import Logger
from time import sleep


def backoff(
          *exceptions,
          logger: Logger,
          start_sleep_time: float = 0.1,
          factor: int = 2,
          border_sleep_time: int = 30,
):
    """Функция для повторного выполнения функции через некоторое время."""
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning("Error. I'll try again in %s seconds.",
                                   sleep_time, exc_info=e)
                    sleep(sleep_time)
                    if sleep_time < border_sleep_time:
                        sleep_time *= factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper
