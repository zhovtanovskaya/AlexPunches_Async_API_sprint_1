"""Подключиться к Кафке."""
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from core.config import config, logger
from utils import messages as msg

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
            logger.warning(
                f'{msg.kafka_unavailable} '
                f'{config.event_store_host}:{config.event_store_port}',
            )
            return None
    return producer
