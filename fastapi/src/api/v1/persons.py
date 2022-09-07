"""
/api/v1/persons/search/
/api/v1/persons/<uuid:UUID>/
/api/v1/persons/<uuid:UUID>/film/
"""
from http import HTTPStatus

from api.v1 import ElasticPaginateSort
from api.v1.shemes.film import FilmShort
from api.v1.shemes.person import Person
from api.v1.shemes.transform_schemes import es_person_to_person_scheme
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from services.person import PersonService, get_person_service

from fastapi import Depends, HTTPException, Query

router = InferringRouter()


@cbv(router)
class FilmCBV:
    person_service: PersonService = Depends(get_person_service)

    @router.get('/search')
    async def person_search(
        self,
        page: ElasticPaginateSort = Depends(),
        query: str | None = Query(default=None),
    ) -> list[Person]:
        if persons := await self.person_service.search():
            return [es_person_to_person_scheme(person) for person in persons]
        return []

    @router.get('/{person_id}')
    async def person_details(
              self,
              person_id: str,
    ) -> Person:
        if person := await self.person_service.get_by_id(person_id):
            return es_person_to_person_scheme(person)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')

    @router.get('/{person_id}/films')
    async def person_films(
        self,
        person_id: str,
        page: ElasticPaginateSort = Depends(),
    ) -> list[FilmShort]:
        pass
