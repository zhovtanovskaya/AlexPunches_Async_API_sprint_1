from typing import Optional
from uuid import UUID

import orjson
from models import orjson_dumps
from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class Person(BaseModel):
    id: UUID
    name: str


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: list
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []
    genres: list[Genre]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
