from enum import Enum
from uuid import UUID

import orjson
from models import orjson_dumps
from pydantic import BaseModel


class Roles(str, Enum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class Person(BaseModel):
    id: UUID
    name: str
    role: list[Roles]
    film_ids: list[UUID]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
