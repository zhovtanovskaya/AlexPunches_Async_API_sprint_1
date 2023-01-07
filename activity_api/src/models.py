"""Модели активностей."""

from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """Декодировать."""
    return orjson.dumps(v, default=default).decode()


class SpawnPointModel(BaseModel):
    """Модель момента фильма, во время просмотра пользователем."""

    user_id: UUID | None = None
    film_id: str
    time: int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
