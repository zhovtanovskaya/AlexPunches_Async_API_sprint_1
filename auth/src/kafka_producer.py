"""Подключиться к Кафке."""
from kafka import KafkaProducer

from core.config import config

producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    """Получить продюсера."""
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=f'{config.event_store_host}:'
                              f'{config.event_store_port}',
        )
    return producer
