from typing import Optional

from pydantic import BaseModel

from api.v1.shemes.genre import GenreShort
from api.v1.shemes.person import PersonShort


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
