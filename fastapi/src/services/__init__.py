from typing import Any, Type

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel


class BaseElasticService:
    def __init__(self,
                 elastic: AsyncElasticsearch,
                 es_index: str,
                 es_model: Type[BaseModel],
                 ):
        self.elastic = elastic
        self.es_index = es_index
        self.es_model = es_model

    async def get_by_id(self, id: str) -> BaseModel | None:
        return await self._get_item_from_elastic(id) or None

    async def _get_item_from_elastic(self, id: str) -> BaseModel | None:
        try:
            doc = await self.elastic.get(self.es_index, id)
        except NotFoundError:
            return None
        return self.es_model(**doc['_source'])

    async def get_all(self) -> list[BaseModel] | None:
        try:
            result = await self.elastic.search(
                index=self.es_index,
                body={'query': {'match_all': {}}}, size=1000,  # noqa TODO как сделать безлимит?
            )
        except NotFoundError:
            return None
        _items = result['hits']['hits']
        return [self.es_model(**_item['_source']) for _item in _items]

    async def search(self) -> Any:
        pass
