import asyncio

from aio_pika import Message
from aiokafka import AIOKafkaConsumer

from src.core.config import settings
from src.db import kafka
from src.etl import etl
from src.mq import rabbitmq


async def startup():
    kafka.consumer = AIOKafkaConsumer(
        settings.kafka.notifications_topic,
        bootstrap_servers=settings.kafka.bootstrap_servers,
        group_id=settings.kafka.notifications_group_id,
    )
    await kafka.consumer.start()

    rabbitmq.connection = await rabbitmq.get_rabbitmq()
    channel = await rabbitmq.connection.channel()
    rabbitmq.exchange = await rabbitmq.get_notification_queue(channel)


async def main():
    try:
        await startup()
        await etl()
    except KeyboardInterrupt:
        await shutdown()


async def shutdown():
    await kafka.consumer.stop()
    await rabbitmq.connection.close()


if __name__ == '__main__':
    asyncio.run(main())

