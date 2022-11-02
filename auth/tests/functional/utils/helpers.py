"""Функции помощники."""

from typing import Any

import orjson


def orjson_dumps(v: Any) -> str:
    """Декодировать orjson.dumps, который возарщает непривычный bytes."""
    return orjson.dumps(v).decode()
