"""Подключиться к Кафке."""
from aiokafka import AIOKafkaProducer

aioproducer: AIOKafkaProducer | None = None


async def get_producer() -> AIOKafkaProducer:
    """Получить продюсера."""
    return aioproducer
