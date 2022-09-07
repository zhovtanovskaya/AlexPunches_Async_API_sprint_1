from functools import lru_cache

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from models.genre import Genre
from services import BaseElasticService

from fastapi import Depends


class GenreService(BaseElasticService):
    pass


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic=elastic, es_index='genres', es_model=Genre)
