"""Подключиться к Кафке."""
from kafka import KafkaProducer

aioproducer: KafkaProducer | None = None


async def get_producer() -> KafkaProducer:
    """Получить продюсера."""
    return aioproducer
