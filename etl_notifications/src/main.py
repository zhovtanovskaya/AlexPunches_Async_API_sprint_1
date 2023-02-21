import asyncio

from aiokafka import AIOKafkaConsumer

from core.config import settings
from db import kafka
from etl import etl


async def startup():
    kafka.consumer = AIOKafkaConsumer(
        settings.kafka.notifications_topic,
        bootstrap_servers=settings.kafka.bootstrap_servers,
        group_id=settings.kafka.notifications_group_id,
    )
    await kafka.consumer.start()


async def main():
    await startup()
    await etl()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
