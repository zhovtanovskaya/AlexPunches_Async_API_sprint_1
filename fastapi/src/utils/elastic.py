from typing import Any, AsyncGenerator, Mapping

from elasticsearch import AsyncElasticsearch


def make_es_sort_name(sort: str) -> str:
    return f'{sort[1:]}:desc' if sort[0] == '-' else f'{sort}:asc'


async def es_scroll_all_pages(
    elastic: AsyncElasticsearch,
    index: str,
    keep_alive: str,
    query: Mapping[str,  Mapping[str, Any]],
    sort: str,
) -> AsyncGenerator:
    if not query:
        query = {'match_all': {}}

    _pit = await elastic.open_point_in_time(index=index, keep_alive=keep_alive)
    _search_after = None
    page = await elastic.search(pit=_pit.raw, query=query, sort=sort,
                                search_after=_search_after)
    while len(page['hits']['hits']):
        yield page
        _search_after = page['hits']['hits'][-1]['sort']
        page = await elastic.search(pit=_pit.raw, query=query, sort=sort,
                                    search_after=_search_after)
