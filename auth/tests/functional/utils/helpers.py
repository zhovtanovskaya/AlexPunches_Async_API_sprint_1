"""Функции помощники."""

from typing import Any, Type

import orjson
from functional.testdata.models import BaseDt


def orjson_dumps(v: Any) -> str:
    """Декодировать orjson.dumps, который возарщает непривычный bytes."""
    return orjson.dumps(v).decode()


def construct_query(table_name: str,
                    data_class: Type[BaseDt],
                    data: list[BaseDt],
                    ):
    """Сформировать данные и SQL-запрос к ним в видет строки."""
    columns = data_class.get_fields()
    stmt = 'INSERT INTO {table_name}'.format(table_name=table_name)
    stmt += ' ({col_str}) '.format(col_str=','.join(columns))
    stmt += ' VALUES ({values_str});'.format(values_str=','.join(['%s'] * len(columns)))  # noqa

    data = [item.as_tuple for item in data]
    return stmt, data
