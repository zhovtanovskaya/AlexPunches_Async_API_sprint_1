from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel

from models import orjson_dumps


class Genre(BaseModel):
    id: UUID
    name: str


class Person(BaseModel):
    id: UUID
    name: str


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: list[str]
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []
    genres: list[Genre]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
