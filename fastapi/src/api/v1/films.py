from http import HTTPStatus

from elasticsearch import BadRequestError
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from api.v1 import SearchEngineSortedPaginate
from api.v1.shemes.film import Film, FilmShort
from api.v1.shemes.transform_schemes import (es_film_to_film_scheme,
                                             es_film_to_film_short_scheme)
from services.film import FilmService, get_film_service
from utils import messages as msg

from fastapi import Depends, HTTPException, Query

router = InferringRouter()


@cbv(router)
class FilmCBV:
    film_service: FilmService = Depends(get_film_service)
    sorted_paginate: SearchEngineSortedPaginate = Depends()

    @router.get('/', summary='Фильтрация по жанру')
    async def film_list(
        self,
        filter_genre: str | None = Query(default=None, alias='filter[genre]'),
    ) -> list[Film]:
        """
        Выбрать все фильмы определенного жанра

        - **filter[genre]**: uuid жанра
        - **sort**: поле для сортировки.
            Можно указать имя поля как в API или как в Эластике.
            - cортировка по вложенным полям через суфикс, например, **.raw**
            - префикс **"-"** для сортировки в обратном порядке.
        - **page[size]**: количество фильмов на одной странице.
        - **page[number]**: номер страницы.
        """
        films = await self.film_service.search(
            sorted_paginate=self.sorted_paginate,
            nested_fields=[('genres', 'id')],
            query=filter_genre,
        )
        return [es_film_to_film_scheme(film) for film in films]

    @router.get('/search',
                summary='Поиск фильмов',
                response_description='Список фильмов с краткой информацией.',
                )
    async def film_search(
        self,
        query: str | None = Query(default=None)
    ) -> list[FilmShort]:
        """
        Поиск фильма по названию.

        - **query**: строка поиска.
        - **sort**: поле для сортировки.
            Можно указать имя поля как в API или как в Эластике.
            - cортировка по вложенным полям через суфикс, например, **.raw**
            - префикс **"-"** для сортировки в обратном порядке.
        - **page[size]**: количество фильмов на одной странице.
        - **page[number]**: номер страницы.
        """
        try:
            films = await self.film_service.search(
                sorted_paginate=self.sorted_paginate,
                query=query,
            )
        except BadRequestError as e:
            raise HTTPException(status_code=e.status_code,
                                detail=f'{msg.bad_request_error} {e.error}')
        return [es_film_to_film_short_scheme(film) for film in films]


@router.get('/{film_id}', response_model=Film, summary='Подробно о фильме')
async def film_details(
          film_id: str,
          film_service: FilmService = Depends(get_film_service),
) -> Film:
    """
    **film_id**: uuid фильма.
    """
    if film := await film_service.get_by_id(film_id):
        return es_film_to_film_scheme(film)
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail=msg.film_not_found_error)
