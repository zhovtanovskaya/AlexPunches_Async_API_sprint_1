from functools import lru_cache

from db.elastic import get_elastic

from api.v1 import SearchEngineSortedPaginate
from api.v1.shemes.film import Film as FilmScheme
from models.film import Film
from services import BaseSearchEngineService
from services.search_engine import AsyncSearchEngine

from fastapi import Depends


class FilmService(BaseSearchEngineService):
    async def search(self,
                     sorted_paginate: SearchEngineSortedPaginate = Depends(),
                     query: str | None = None,
                     search_fields: str | None = None,
                     nested_fields: list[tuple[str, str]] | None = None,
                     ) -> list[Film]:

        if query and nested_fields is not None:
            dsl = super()._make_search_nested_dsl(
                query=query, path_fields=nested_fields)
        else:
            dsl = super()._make_search_dsl(
                query=query, search_fields=search_fields)
        sorted_paginate.sort = super()._make_es_sort(
            api_field=sorted_paginate.sort,
            api_scheme=FilmScheme,
        )

        films_page = await super().pagination_search(
            sorted_paginate=sorted_paginate,
            dsl=dsl,
        )
        return [
            Film.parse_obj(film['_source'])
            for film in films_page['hits']['hits']
        ]


@lru_cache()
def get_film_service(
        search_engine: AsyncSearchEngine = Depends(get_elastic),
) -> FilmService:
    return FilmService(search_engine, es_index='movies', es_model=Film)
