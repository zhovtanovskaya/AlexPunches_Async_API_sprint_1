from http import HTTPStatus
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class Genre(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str

    class Config:
        allow_population_by_field_name = True


class Person(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')

    class Config:
        allow_population_by_field_name = True


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[list[Genre]]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


@router.get('/{film_id}', response_model=Film)
async def film_details(
          film_id: str,
          film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')

    return Film(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[Genre(**genre.dict()) for genre in film.genres],
        actors=[Person(**actor.dict()) for actor in film.actors],
        writers=[Person(**writer.dict()) for writer in film.writers],
        directors=[Person(**director.dict()) for director in film.directors],
    )
