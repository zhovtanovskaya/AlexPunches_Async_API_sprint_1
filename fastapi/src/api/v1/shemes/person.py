from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PersonShort(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')

    class Config:
        allow_population_by_field_name = True


class FilmShort(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


class Person(PersonShort):
    role: Optional[list[str]]
    film_ids: Optional[list[UUID]]

    class Config:
        allow_population_by_field_name = True
