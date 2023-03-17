from pathlib import PurePosixPath
from urllib.parse import parse_qs, unquote, urlparse


def get_query_param(path, key):
    query = urlparse(path).query
    params = parse_qs(query)
    values = params.get(key, [])
    if len(values) == 1:
        return values[0]


def get_room_id_by_path(path):
    try:
        return PurePosixPath(unquote(urlparse(path).path)).parts[1]
    except IndexError:
        return None
