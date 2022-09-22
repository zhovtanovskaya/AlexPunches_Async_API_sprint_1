from core.config import config
from pydantic import PositiveInt

from fastapi import Depends, Query


class ElasticPaginate:
    def __init__(self,
                 number: PositiveInt = Query(default=1, alias='page[number]'),
                 size: PositiveInt = Query(default=50, alias='page[size]'),
                 ):
        self.number = number
        self.size = size


class ElasticPaginateSort:
    def __init__(self,
                 page: ElasticPaginate = Depends(),
                 sort: str | None = Query(default=config.elastic_default_sort),
                 ):
        self.sort = sort
        self.page = page
