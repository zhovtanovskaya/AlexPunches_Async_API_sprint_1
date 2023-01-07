"""Очистить все шарды кликхауса."""
import os
import sys

from clickhouse_driver import Client

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
sys.path.append(BASE_DIR)

from config import settings


def run() -> None:
    """Запуск."""
    for port in settings.ch_ports:
        client = Client(host=settings.ch_host, port=port)
        client.execute('TRUNCATE TABLE shard.test')


if __name__ == '__main__':
    run()
