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
                     ) -> list[Film]:
        if query:
            dsl = {'match': {'title': query}}
        else:
            dsl = {'match_all': {}}
        films_page = await super().get_search_es_page(
            page_size=page_size,
            page_number=page_number,
            dsl=dsl,
            es_scheme=FilmScheme,
            sort=sort,
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
