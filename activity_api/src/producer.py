"""Подключиться к Кафке."""
import asyncio

from aiokafka import AIOKafkaProducer

from core.config import config

loop = asyncio.get_event_loop()

print(config.event_store_host, config.event_store_port)
aioproducer = AIOKafkaProducer(
    loop=loop,
    client_id=config.project_name,
    bootstrap_servers=f'{config.event_store_host}:{config.event_store_port}',
)


async def get_producer() -> AIOKafkaProducer:
    """Получить продюсера."""
    return aioproducer
