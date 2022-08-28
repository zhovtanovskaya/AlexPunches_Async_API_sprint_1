"""
/api/v1/genres/
/api/v1/genres/<uuid:UUID>/
"""
from http import HTTPStatus
from uuid import UUID

from pydantic import BaseModel, Field
from services.genre import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class Genre(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str

    class Config:
        allow_population_by_field_name = True


@router.get('/')
async def genres_list(
          genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genres = await genre_service.get_all()
    return [Genre(uuid=genre.id, name=genre.name) for genre in genres]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
          genre_id: str,
          genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')

    return Genre(
        uuid=genre.id,
        name=genre.name,
    )
