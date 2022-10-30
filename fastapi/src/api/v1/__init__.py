from pydantic import PositiveInt

from core.config import config

from fastapi import Depends, Query


class SearchEnginePaginate:
    def __init__(self,
                 size: PositiveInt = Query(default=50, alias='page[size]'),
                 number: PositiveInt = Query(default=1, alias='page[number]'),
                 ):
        self.size = size
        self.number = number


class SearchEngineSortedPaginate:
    def __init__(self,
                 page: SearchEnginePaginate = Depends(),
                 sort: str | None = Query(default=config.elastic_default_sort),
                 ):
        self.sort = sort
        self.page = page
