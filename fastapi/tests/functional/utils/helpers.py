import orjson


def orjson_dumps(v):
    return orjson.dumps(v).decode()
