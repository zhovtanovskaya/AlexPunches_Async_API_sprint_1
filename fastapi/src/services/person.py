from functools import lru_cache
from typing import Mapping

from api.v1.shemes.person import Person as PersonScheme
from core.config import config
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from models.film import Film
from models.person import Person
from pydantic import BaseModel
from services import BaseElasticService, NotFoundElasticError
from utils.elastic import es_scroll_all_pages, make_es_sort_name

from fastapi import Depends


class PersonService(BaseElasticService):
    async def get_by_id(self, id: str) -> BaseModel | None:
        if person := await super()._get_item_from_elastic(id):
            films = await self._get_all_films_for_persons([person['id']])
            params = self._get_person_param_from_films_list(person['id'],
                                                            films)
            person['film_ids'] = params.get('film_ids')
            person['role'] = params.get('role')
            return self.es_model.parse_obj(person)
        return None

    async def search(self,
                     page_size: int,
                     page_number: int,
                     sort: str = config.elastic_default_sort,
                     query: str | None = None,
                     ) -> list[BaseModel]:
        if query:
            dsl = {'match': {'name': query}}
        else:
            dsl = {'match_all': {}}
        persons_page = await super().get_search_es_page(
            page_size=page_size,
            page_number=page_number,
            dsl=dsl,
            es_scheme=PersonScheme,
            sort=sort,
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
        if not await super()._get_item_from_elastic(person_id):
            raise NotFoundElasticError()
        films = await self._get_all_films_for_persons([person_id])
        return [Film.parse_obj(film) for film in films]

    async def _get_all_films_for_persons(self,
                                         persons_ids: list[str],
                                         ) -> list[Mapping]:
        query = {
            "bool": {
                "should": [
                    {"nested": {
                            "path": "writers",
                            "query": {"terms": {"writers.id": persons_ids}}
                    }},
                    {"nested": {
                            "path": "directors",
                            "query": {"terms": {"directors.id": persons_ids}}
                    }},
                    {"nested": {
                            "path": "actors",
                            "query": {"terms": {"actors.id": persons_ids}}
                    }},
                ]
            }
        }
        films_pages = es_scroll_all_pages(
            elastic=self.elastic,
            index='movies',
            keep_alive=config.elastic_keep_alive,
            query=query,
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
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic=elastic, es_index='persons', es_model=Person)
