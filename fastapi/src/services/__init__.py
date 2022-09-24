from typing import Any, Mapping, Type

from api.v1 import ElasticSortedPaginate
from api.v1.shemes.transform_schemes import api_field_name_to_es_field_name
from core.config import config
from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from utils.elastic import (es_scroll_all_pages, get_one_page_from_elastic,
                           make_es_sort_name)

from fastapi import Depends


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

    async def get_all_from_elastic(
              self,
              sort: str = config.elastic_default_sort,
              keep_alive: str = config.elastic_keep_alive,
              dsl: Mapping[str,  Mapping[str, Any]] | None = None,
          ) -> list[BaseModel]:

        sort = make_es_sort_name(sort)
        pages = es_scroll_all_pages(
            elastic=self.elastic,
            index=self.es_index,
            keep_alive=keep_alive,
            dsl=dsl,
            sort=sort,
        )

        items = []
        async for page in pages:
            for item in page['hits']['hits']:
                items.append(self.es_model.parse_obj(item['_source']))
        return items

    async def pagination_search(
        self,
        sorted_paginate: ElasticSortedPaginate = Depends(),
        dsl: Mapping[str,  Mapping[str, Any]] | None = None,
    ) -> ObjectApiResponse:

        return await get_one_page_from_elastic(
            elastic=self.elastic,
            index=self.es_index,
            sorted_paginate=sorted_paginate,
            dsl=dsl,
        )

    @staticmethod
    def _make_es_sort(api_field: str, api_scheme: Type[BaseModel]):
        sort = api_field_name_to_es_field_name(api_field_name=api_field,
                                               api_scheme=api_scheme)
        return make_es_sort_name(sort)

    def _make_search_dsl(self,
                         search_fields: str | None = None,
                         query: str | None = None,
                         ):
        if search_fields is None:
            search_fields = config.es_indexes[self.es_index].search_field
        fields = search_fields.split(',')
        if query:
            return {'bool': {
                'should': [{'match': {field: query}} for field in fields]
            }}
        return {'match_all': {}}

    @staticmethod
    def _make_search_nested_dsl(
              path_fields: list[tuple[str, str]],
              query: str | list[str],
            ):
        type_term = 'terms' if type(query) == list else 'term'
        return {"bool": {"should": [
               {"nested": {"path": path_field[0], "query": {
                    type_term: {f"{path_field[0]}.{path_field[1]}": query}}}}
               for path_field in path_fields]}}
