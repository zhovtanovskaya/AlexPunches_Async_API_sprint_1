from typing import Optional

from api.v1.shemes.genre import GenreShort
from api.v1.shemes.person import PersonShort
from pydantic import BaseModel


class FilmShort(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


class Film(FilmShort):
    description: Optional[str]
    genre: Optional[list[GenreShort]]
    actors: list[PersonShort]
    writers: list[PersonShort]
    directors: list[PersonShort]
