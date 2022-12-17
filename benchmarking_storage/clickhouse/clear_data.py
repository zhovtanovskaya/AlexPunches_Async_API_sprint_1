"""Очистить все шарды кликхауса."""
from clickhouse_driver import Client
from config import settings


def run() -> None:
    """Запуск."""
    for port in settings.ch_ports:
        client = Client(host=settings.ch_host, port=port)
        client.execute('TRUNCATE TABLE shard.test')


if __name__ == '__main__':
    run()
