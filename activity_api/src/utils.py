import orjson


def orjson_dumps(v, *, default):
    """Декодировать."""
    return orjson.dumps(v, default=default).decode()
