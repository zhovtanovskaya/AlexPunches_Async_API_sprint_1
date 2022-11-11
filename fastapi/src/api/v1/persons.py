from http import HTTPStatus

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from api.v1 import SearchEngineSortedPaginate
from api.v1.shemes.film import FilmShort
from api.v1.shemes.person import Person
from api.v1.shemes.transform_schemes import (es_film_to_film_short_scheme,
                                             es_person_to_person_scheme)
from fastapi import Depends, HTTPException, Query
from services import NotFoundSearchEngineError
from services.person import PersonService, get_person_service
from utils import messages as msg

router = InferringRouter()


@cbv(router)
class FilmCBV:
    person_service: PersonService = Depends(get_person_service)

    @router.get('/search', summary='Поиск персон')
    async def person_search(
        self,
        query: str | None = Query(default=None),
        sorted_paginate: SearchEngineSortedPaginate = Depends(),
    ) -> list[Person]:
        """
        Поиск персоны по имени.

        - **query**: строка поиска.
        - **sort**: поле для сортировки.
            Можно указать имя поля как в API или как в Эластике.
            - cортировка по вложенным полям через суфикс, например, **.raw**
            - префикс **"-"** для сортировки в обратном порядке.
        - **page[size]**: количество фильмов на одной странице.
        - **page[number]**: номер страницы.
        """
        persons = await self.person_service.search(
                            sorted_paginate=sorted_paginate,
                            query=query,
                        )
        return [es_person_to_person_scheme(person) for person in persons]

    @router.get('/{person_id}', summary='Подробно о персоне')
    async def person_details(self, person_id: str) -> Person:
        """
        **person_id**: uuid Персоны.
        """
        if person := await self.person_service.get_by_id(person_id):
            return es_person_to_person_scheme(person)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=msg.person_not_found_error)

    @router.get('/{person_id}/films',
                summary='Фильмы с персоной',
                response_description='Список фильмов с краткой информацией.',
                )
    async def person_films(self, person_id: str) -> list[FilmShort]:
        """
        Все фильмы с участием персоны.

        **person_id**: uuid Персоны.
        """
        try:
            films = await self.person_service.get_films_by_person(person_id)
        except NotFoundSearchEngineError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail=msg.person_not_found_error)
        return [es_film_to_film_short_scheme(film) for film in films]
