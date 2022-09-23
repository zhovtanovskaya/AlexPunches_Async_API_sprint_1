from functools import lru_cache

from api.v1.shemes.film import Film as FilmScheme
from core.config import config
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from models.film import Film
from services import BaseElasticService

from fastapi import Depends


class FilmService(BaseElasticService):
    async def search(self,
                     page_size: int,
                     page_number: int,
                     sort: str = config.elastic_default_sort,
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
        sort = super()._make_es_sort(api_field=sort, api_scheme=FilmScheme)

        films_page = await super().pagination_search(
            page_size=page_size,
            page_number=page_number,
            sort=sort,
            dsl=dsl,
        )
        return [
            Film.parse_obj(film['_source'])
            for film in films_page['hits']['hits']
        ]


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic, es_index='movies', es_model=Film)
