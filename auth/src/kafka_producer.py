"""Подключиться к Кафке."""
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from core.config import config

producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    """Получить продюсера."""
    global producer
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=f'{config.event_store_host}:'
                                  f'{config.event_store_port}',
            )
        except NoBrokersAvailable:
            return None
    return producer
