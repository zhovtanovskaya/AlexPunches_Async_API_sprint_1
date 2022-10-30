from functools import lru_cache

from db.elastic import get_elastic

from models.genre import Genre
from services import BaseSearchEngineService
from services.search_engine import AsyncSearchEngine

from fastapi import Depends


class GenreService(BaseSearchEngineService):

    async def get_all_genres(self):
        pages = await super().get_all_from_search_engine()
        items = []
        async for page in pages:
            for item in page['hits']['hits']:
                items.append(self.es_model.parse_obj(item['_source']))
        return items


@lru_cache()
def get_genre_service(
        search_engine: AsyncSearchEngine = Depends(get_elastic),
) -> GenreService:
    return GenreService(search_engine=search_engine,
                        es_index='genres', es_model=Genre)
