from typing import Any, Coroutine

from aio_pika import Message
from aio_pika.abc import AbstractQueue
from aiokafka import AIOKafkaConsumer

from src.core.config import settings
from src.db.kafka import get_kafka_consumer
from src.extract.extractor import extract
from src.mq.rabbitmq import get_rabbitmq_exchange
from src.transform.users import UserSignedUpTransformer


async def etl():
    consumer: AIOKafkaConsumer = await get_kafka_consumer()
    exchange: Coroutine[Any, Any, AbstractQueue] = \
        await get_rabbitmq_exchange()
    transformer = UserSignedUpTransformer()
    async for event in extract(consumer):
        print(event)
        async for posting in transformer.make_postings(event):
            message = Message(body=posting.json_bytes())
            await exchange.publish(
                message, routing_key=settings.rabbitmq.queue_name,
            )
