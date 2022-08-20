import more_itertools
from psycopg2.extras import DictRow
from typing import Generator

import orjson
import requests
from config import EsIndex, settings
from postgres_to_es import DbConnect
from postgres_to_es.elastic_index_state import (ElasticIndexState,
                                                ElasticIndexStateError)
from postgres_to_es.services import ElasticInsertError


class PostgresExtracter(DbConnect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_state = self.create_es_state()

    def extract_movie_data(self,
                           es_index: EsIndex
                           ) -> Generator[DictRow, None, None]:
        """Получить данные обновленных фильмов."""
        self.cursor.execute(
            es_index.sql,
            {'timestamp': self.es_state.get_last_time(es_index.name)}
        )
        while fetched := self.cursor.fetchmany(settings.bunch_extract):
            yield from fetched

    def create_es_state(self):
        try:
            return ElasticIndexState(self.connection)
        except Exception as e:
            raise ElasticIndexStateError() from e


class ElasticLoader:
    @classmethod
    def save_data(cls,
                  data: Generator[DictRow, None, None],
                  es_index: EsIndex,
                  ) -> int:
        """Записать данные в Elastic."""
        count = 0
        headers = {'Content-Type': 'application/x-ndjson'}
        for items in more_itertools.ichunked(data, settings.bunch_es_load):
            bulk_items = ''.join([
                cls._make_es_item_for_bulk(item, es_index)
                for item in items
            ])

            try:
                r = requests.put(f'{settings.es_base_url}/_bulk',
                                 headers=headers,
                                 data=bulk_items,
                                 )
                pass
            except requests.exceptions.ConnectionError as e:
                raise ElasticInsertError() from e
            if r.status_code == 200:
                if r.json().get('items') is not None:
                    count += len(r.json().get('items'))
            else:
                raise ElasticInsertError("Can't insert data into Elastic. "
                                         "Status_code: %s ", r.status_code)
        return count

    @staticmethod
    def _make_es_item_for_bulk(row: DictRow, es_index: EsIndex) -> str:
        """
        Сделать пару строк[json-объектов] для Bulk-запроса в Elasticsearch
        :param row: DictRow из постгреса
        :param es_index: EsIndex
        :return: str, пара json-объектов в виде строк,
            вторая строка - это EsModel,
            пример:
            {"index": {"_index": "es_index_name", "_id": "my_id"}}
            {"field1": "1", "field2": "2"}
        PS
        перенос строки "\n" должен быть у каждой, даже самой последней.
        """
        es_index_str = {'_index': es_index.name, '_id': row['id']}
        es_item = orjson.dumps({'index': es_index_str}).decode("utf-8") + '\n'

        movie_obj = es_index.es_model.parse_obj(row)
        es_item += movie_obj.json() + '\n'
        return es_item
