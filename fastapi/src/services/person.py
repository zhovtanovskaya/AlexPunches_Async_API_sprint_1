from functools import lru_cache
from typing import Mapping

from fastapi import Depends
from pydantic import BaseModel

from api.v1 import SearchEngineSortedPaginate
from api.v1.shemes.person import Person as PersonScheme
from core.config import config
from db.elastic import get_elastic
from models.film import Film
from models.person import Person
from services import BaseSearchEngineService, NotFoundSearchEngineError
from services.search_engine import AsyncSearchEngine
from utils.search_engine import es_scroll_all_pages, make_es_sort_name


class PersonService(BaseSearchEngineService):
    async def get_by_id(self, id: str) -> BaseModel | None:
        if person := await super()._get_item_from_search_engine(id):
            films = await self._get_all_films_for_persons([person['id']])
            params = self._get_person_param_from_films_list(person['id'],
                                                            films)
            person['film_ids'] = params.get('film_ids')
            person['role'] = params.get('role')
            return self.es_model.parse_obj(person)
        return None

    async def search(self,
                     sorted_paginate: SearchEngineSortedPaginate = Depends(),
                     query: str | None = None,
                     search_fields: str | None = None,
                     ) -> list[BaseModel]:
        dsl = super()._make_search_dsl(query=query,
                                       search_fields=search_fields)
        sorted_paginate.sort = super()._make_es_sort(
            api_field=sorted_paginate.sort,
            api_scheme=PersonScheme,
        )

        persons_page = await super().pagination_search(
            sorted_paginate=sorted_paginate,
            dsl=dsl,
        )
        persons = [
            person['_source'] for person in persons_page['hits']['hits']
        ]
        persons_ids = [person['id'] for person in persons]
        films = await self._get_all_films_for_persons(persons_ids)

        for person in persons:
            params = self._get_person_param_from_films_list(person['id'],
                                                            films)
            person['film_ids'] = params['film_ids']
            person['role'] = params['role']

        return [self.es_model.parse_obj(person) for person in persons]

    async def get_films_by_person(self, person_id: str) -> list[BaseModel]:
        if not await super()._get_item_from_search_engine(person_id):
            raise NotFoundSearchEngineError()
        films = await self._get_all_films_for_persons([person_id])
        return [Film.parse_obj(film) for film in films]

    async def _get_all_films_for_persons(self,
                                         persons_ids: list[str],
                                         ) -> list[Mapping]:
        nested_fields = [
            ('writers', 'id'), ('directors', 'id'), ('actors', 'id')
        ]
        dsl = super()._make_search_nested_dsl(
                query=persons_ids, path_fields=nested_fields
            )
        films_pages = es_scroll_all_pages(
            search_engine=self.search_engine,
            index=config.es_indexes['movies'].name,
            keep_alive=config.elastic_keep_alive,
            dsl=dsl,
            sort=make_es_sort_name(config.elastic_default_sort),
        )
        films = []
        async for page in films_pages:
            for film in page['hits']['hits']:
                films.append(film['_source'])
        return films

    @staticmethod
    def _get_person_param_from_films_list(person_id: str,
                                          films: list,
                                          ) -> Mapping[str, set[str]]:
        person: Mapping[str, set[str]] = {
            'film_ids': set(),
            'role': set(),
        }
        for film in films:
            if _thereis_id_in_list_obj(person_id, film['writers']):
                person['film_ids'].add(film['id'])
                person['role'].add('writer')
            if _thereis_id_in_list_obj(person_id, film['directors']):
                person['film_ids'].add(film['id'])
                person['role'].add('director')
            if _thereis_id_in_list_obj(person_id, film['actors']):
                person['film_ids'].add(film['id'])
                person['role'].add('actor')
        return person


def _thereis_id_in_list_obj(id: str, list_obj: list[Mapping[str, str]]):
    for obj in list_obj:
        if obj['id'] == id:
            return True
    return False


@lru_cache()
def get_person_service(
        search_engine: AsyncSearchEngine = Depends(get_elastic),
) -> PersonService:
    return PersonService(search_engine=search_engine,
                         es_index='persons', es_model=Person)
