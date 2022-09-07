from functools import lru_cache

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from models.person import Person
from services import BaseElasticService

from fastapi import Depends


class PersonService(BaseElasticService):
    pass


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic=elastic, es_index='persons', es_model=Person)
