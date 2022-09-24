from typing import Any, AsyncGenerator, Mapping

from api.v1 import ElasticSortedPaginate
from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from fastapi import Depends


def make_es_sort_name(sort: str) -> str:
    return f'{sort[1:]}:desc' if sort[0] == '-' else f'{sort}:asc'


async def es_scroll_all_pages(
    elastic: AsyncElasticsearch,
    index: str,
    keep_alive: str,
    dsl: Mapping[str,  Mapping[str, Any]],
    sort: str,
) -> AsyncGenerator:

    _pit = await elastic.open_point_in_time(index=index, keep_alive=keep_alive)
    _search_after = None
    page = await elastic.search(pit=_pit.raw, query=dsl, sort=sort,
                                search_after=_search_after)
    while len(page['hits']['hits']):
        yield page
        _search_after = page['hits']['hits'][-1]['sort']
        page = await elastic.search(pit=_pit.raw, query=dsl, sort=sort,
                                    search_after=_search_after)


async def get_one_page_from_elastic(
          elastic: AsyncElasticsearch,
          index: str,
          dsl: Mapping[str, Any],
          sorted_paginate: ElasticSortedPaginate = Depends(),
      ) -> ObjectApiResponse:

    from_ = sorted_paginate.page.size * (sorted_paginate.page.number - 1)

    return await elastic.search(
        index=index,
        query=dsl,
        sort=sorted_paginate.sort,
        from_=from_,
        size=sorted_paginate.page.size,
    )
