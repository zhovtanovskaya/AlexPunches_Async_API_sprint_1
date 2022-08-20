import logging
from typing import Any

from postgres_to_es.data_scheme import (GenreEsModel, MovieEsModel,
                                        PersonEsModel)
from postgres_to_es.sqls.pg_2_es_sql import (film_work_2_es, genre_2_es,
                                             person_2_es)
from pydantic import BaseSettings, DirectoryPath, Field, FilePath

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Dsl(BaseSettings):
    dbname: str = Field(..., env='postgres_db')
    user: str = Field('app', env='postgres_user')
    password: str = Field(..., env='postgres_password')
    host: str = Field('127.0.0.1', env='db_host')
    port: str = Field(5432, env='db_port')


class EsBaseUrl(BaseSettings):
    es_host: str = Field(..., env='es_host')
    es_port: str = Field(9200, env='es_port')

    def get_url(self):
        return 'http://{}:{}'.format(self.es_host, self.es_port)


class EsIndex(BaseSettings):
    """Класс описания индекса Эластика."""
    name: str
    json_scheme: str
    sql: str
    es_model: Any  # TODO какой тут тип сделать?


class BaseConfig(BaseSettings):
    bunch_extract: int = 100
    bunch_insert: int = 100
    bunch_es_load: int = 100
    sqlite3_path: FilePath = Field(..., env='sqlite3_path')
    es_schemas_dir: DirectoryPath = Field(..., env='es_schemas_dir')
    es_base_url: str = EsBaseUrl().get_url()
    dsl: dict = Dsl().dict()
    es_indexes: list[EsIndex] = [
        EsIndex(name='movies',
                json_scheme='movies.json',
                sql=film_work_2_es,
                es_model=MovieEsModel,
                ),
        EsIndex(name='genre',
                json_scheme='genres.json',
                sql=genre_2_es,
                es_model=GenreEsModel,
                ),
        EsIndex(name='person',
                json_scheme='persons.json',
                sql=person_2_es,
                es_model=PersonEsModel,
                ),
    ]


settings = BaseConfig()
