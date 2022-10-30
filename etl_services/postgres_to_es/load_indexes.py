import os
import sys
import time
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from config import EsIndex, logger, settings
from postgres_to_es.add_es_schemas import add_es_index, check_es_index
from postgres_to_es.loaders import ElasticLoader, PostgresExtracter
from postgres_to_es.services import ElasticInsertError, backoff


@backoff(psycopg2.OperationalError, Exception, logger=logger)
@contextmanager
def connect_to_postgress(connect_params: dict):
    conn = None
    try:
        conn = psycopg2.connect(**connect_params, cursor_factory=DictCursor)
        yield conn
    finally:
        if conn is not None:
            conn.close()


@backoff(ElasticInsertError, logger=logger)
def load_from_postgres(
          pg_connect: _connection,
          es_index: EsIndex,
) -> None:
    """Основной метод загрузки данных из Postgres в Elasticsearch."""
    pg_extracter = PostgresExtracter(pg_connect)
    data = pg_extracter.extract_movie_data(es_index=es_index)
    loaded_count = ElasticLoader.save_data(data=data, es_index=es_index)
    logger.info('Проиндексировано %s в схему %s.', loaded_count, es_index.name)
    pg_extracter.es_state.set_last_time(key=es_index.name)


if __name__ == '__main__':
    with (connect_to_postgress(settings.dsl) as pg_conn):
        while True:
            for index in settings.es_indexes:
                if not check_es_index(index.name):
                    add_es_index(
                        index.name,
                        f'{settings.es_schemas_dir}/{index.json_scheme}',
                    )

                load_from_postgres(pg_conn, es_index=index)
            time.sleep(10)
