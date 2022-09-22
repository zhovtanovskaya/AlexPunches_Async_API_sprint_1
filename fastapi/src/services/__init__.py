from typing import Any, Mapping, Type

from api.v1.shemes.transform_schemes import api_field_name_to_es_field_name
from core.config import config
from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from utils.elastic import es_scroll_all_pages, make_es_sort_name


class NotFoundElasticError(Exception):
    ...


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
        if source := await self._get_item_from_elastic(id):
            return self.es_model.parse_obj(source)
        return None

    async def _get_item_from_elastic(self, id: str) -> Any | None:
        try:
            doc = await self.elastic.get(index=self.es_index, id=id)
        except NotFoundError:
            return None
        return doc['_source']

    async def get_all(
              self,
              sort: str = config.elastic_default_sort,
              keep_alive: str = config.elastic_keep_alive,
              query: Mapping[str,  Mapping[str, Any]] | None = None,
          ) -> list[BaseModel]:

        sort = make_es_sort_name(sort)
        pages = es_scroll_all_pages(
            elastic=self.elastic,
            index=self.es_index,
            keep_alive=keep_alive,
            query=query,
            sort=sort,
        )

        items = []
        async for page in pages:
            for item in page['hits']['hits']:
                items.append(self.es_model.parse_obj(item['_source']))
        return items

    async def get_search_es_page(
              self,
              page_size: int,
              page_number: int,
              dsl: Mapping[str, Any],
              es_scheme: Type[BaseModel],
              sort: str = config.elastic_default_sort,
          ) -> ObjectApiResponse:
        sort = api_field_name_to_es_field_name(api_field_name=sort,
                                               es_scheme=es_scheme)
        sort = make_es_sort_name(sort)

        from_ = page_size * (page_number - 1)

        return await self.elastic.search(
            index=self.es_index,
            query=dsl,
            sort=sort,
            from_=from_,
            size=page_size,
        )
