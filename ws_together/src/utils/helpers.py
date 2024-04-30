from pathlib import PurePosixPath
from urllib.parse import parse_qs, unquote, urlparse

import orjson


def orjson_dumps(v):
    return orjson.dumps(v).decode()


def get_query_param(path, key):
    query = urlparse(path).query
    params = parse_qs(query)
    values = params.get(key, [])
    if len(values) == 1:
        return values[0]


def get_room_id_by_path(path):
    """Получить рум_ид.

    В строке типа '/room/{room_id}' это будет parts[2]
    """
    try:
        return PurePosixPath(unquote(urlparse(path).path)).parts[2]
    except IndexError:
        return None
