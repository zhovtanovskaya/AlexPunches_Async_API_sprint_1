from functools import lru_cache
from typing import Optional

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.genre import Genre

from fastapi import Depends


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_elastic(genre_id)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genre', genre_id)

        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def get_all(self) -> list[Genre]:
        try:
            result = await self.elastic.search(
                index='genre',
                body={'query': {'match_all': {}}}, size=999,
            )
        except NotFoundError:
            return None
        _genres = result['hits']['hits']
        return [Genre(**_genre['_source']) for _genre in _genres]


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
