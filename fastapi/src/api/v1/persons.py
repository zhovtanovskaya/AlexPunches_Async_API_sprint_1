from http import HTTPStatus

from api.v1 import ElasticPaginateSort
from api.v1.shemes.film import FilmShort
from api.v1.shemes.person import Person
from api.v1.shemes.transform_schemes import (es_film_to_film_short_scheme,
                                             es_person_to_person_scheme)
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from services import NotFoundElasticError
from services.person import PersonService, get_person_service

from fastapi import Depends, HTTPException, Query

router = InferringRouter()


@cbv(router)
class FilmCBV:
    person_service: PersonService = Depends(get_person_service)

    @router.get('/search')
    async def person_search(
        self,
        query: str | None = Query(default=None),
        params: ElasticPaginateSort = Depends(),
    ) -> list[Person]:
        persons = await self.person_service.search(
                            page_size=params.page.size,
                            page_number=params.page.number,
                            sort=params.sort,
                            query=query,
                        )
        return [es_person_to_person_scheme(person) for person in persons]

    @router.get('/{person_id}')
    async def person_details(self, person_id: str) -> Person:
        if person := await self.person_service.get_by_id(person_id):
            return es_person_to_person_scheme(person)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Person not found')

    @router.get('/{person_id}/films')
    async def person_films(self, person_id: str) -> list[FilmShort]:
        try:
            films = await self.person_service.get_films_by_person(person_id)
        except NotFoundElasticError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail='Person not found')
        return [es_film_to_film_short_scheme(film) for film in films]
