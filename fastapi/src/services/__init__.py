from typing import Any, Mapping, Type

from elastic_transport import ObjectApiResponse
from pydantic import BaseModel

from api.v1 import SearchEngineSortedPaginate
from api.v1.shemes.transform_schemes import api_field_name_to_es_field_name
from core.config import config
from fastapi import Depends
from services.search_engine import AsyncSearchEngine
from utils.search_engine import (es_scroll_all_pages,
                                 get_one_page_from_search_engine,
                                 make_es_sort_name)


class NotFoundSearchEngineError(Exception):
    ...


class BaseSearchEngineService:
    def __init__(self,
                 search_engine: AsyncSearchEngine,
                 es_index: str,
                 es_model: Type[BaseModel],
                 ):
        self.search_engine = search_engine
        self.es_index = es_index
        self.es_model = es_model

    async def get_by_id(self, id: str) -> BaseModel | None:
        if source := await self._get_item_from_search_engine(id):
            return self.es_model.parse_obj(source)
        return None

    async def _get_item_from_search_engine(self, id: str) -> Any | None:
        try:
            doc = await self.search_engine.get(index=self.es_index, id=id)
        except Exception:
            return None
        return doc['_source']

    async def get_all_from_search_engine(
              self,
              sort: str = config.elastic_default_sort,
              keep_alive: str = config.elastic_keep_alive,
              dsl: Mapping[str,  Mapping[str, Any]] | None = None,
          ) -> list[ObjectApiResponse]:

        sort = make_es_sort_name(sort)
        pages = es_scroll_all_pages(
            search_engine=self.search_engine,
            index=self.es_index,
            keep_alive=keep_alive,
            dsl=dsl,
            sort=sort,
        )
        return pages

    async def pagination_search(
        self,
        sorted_paginate: SearchEngineSortedPaginate = Depends(),
        dsl: Mapping[str,  Mapping[str, Any]] | None = None,
    ) -> ObjectApiResponse:

        return await get_one_page_from_search_engine(
            search_engine=self.search_engine,
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
