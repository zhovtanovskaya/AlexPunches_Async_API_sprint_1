from fastapi import Depends, Query


class ElasticPaginate:
    def __init__(self,
                 number: int = Query(default=1, alias='page[number]'),
                 size: int = Query(default=50, alias='page[size]'),
                 ):
        self.number = number
        self.size = size


class ElasticPaginateSort:
    def __init__(self,
                 page: ElasticPaginate = Depends(),
                 sort: str | None = Query(default=None),
                 ):
        self.sort = sort
