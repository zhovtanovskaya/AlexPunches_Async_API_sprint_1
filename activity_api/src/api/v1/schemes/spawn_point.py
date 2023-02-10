"""Пидантик-схемы активностей."""
import orjson
from pydantic import BaseModel

from src.utils import orjson_dumps


class SpawnPointScheme(BaseModel):
    """Схема момента фильма, во время просмотра пользователем.

    Каждую минуту клиен отправляет данные, на каком моменте в данный момент
    находится просмотр фильма.
    Если пользователь аутентифицирован, то передается и юзер-ид.
    """

    film_id: str
    time: int

    class Config:  # noqa
        json_loads = orjson.loads
        json_dumps = orjson_dumps
