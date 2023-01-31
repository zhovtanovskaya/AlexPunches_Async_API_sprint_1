"""Удобные утилиты."""
from contextvars import ContextVar

import orjson

request_id: ContextVar[str] = ContextVar('request_id', default='')


def orjson_dumps(v, *, default):
    """Декодировать."""
    return orjson.dumps(v, default=default).decode()
