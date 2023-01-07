"""Пидантик-схемы активностей."""
from uuid import UUID

import orjson
from pydantic import BaseModel

from utils import orjson_dumps


class SpawnPointScheme(BaseModel):
    """Схема момента фильма, во время просмотра пользователем.

    Каждую минуту клиен отправляет данные, на каком моменте в данный момент
    находится просмотр фильма.
    Если пользователь аутентифицирован, то передается и юзер-ид.
    """

    user_id: UUID | None = None
    film_id: str
    time: int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
