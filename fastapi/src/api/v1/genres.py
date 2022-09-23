from http import HTTPStatus

from api.v1.shemes.genre import Genre
from api.v1.shemes.transform_schemes import es_genre_to_genre_scheme
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from services.genre import GenreService, get_genre_service

from fastapi import Depends, HTTPException

router = InferringRouter()


@cbv(router)
class FilmCBV:
    genre_service: GenreService = Depends(get_genre_service)

    @router.get('/')
    async def genres_list(self) -> list[Genre]:
        genres = await self.genre_service.get_all_from_elastic()
        return [es_genre_to_genre_scheme(genre) for genre in genres]

    @router.get('/{genre_id}', response_model=Genre)
    async def genre_details(self, genre_id: str) -> Genre:
        if genre := await self.genre_service.get_by_id(genre_id):
            return es_genre_to_genre_scheme(genre)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')
