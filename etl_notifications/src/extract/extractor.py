from typing import AsyncIterable

from aiokafka import AIOKafkaConsumer
from extract.models.protocols import Event
from extract.models.user_events import UserCreatedEvent


class Extractor:

    async def extract(self) -> AsyncIterable[UserCreatedEvent]:
        consumer = AIOKafkaConsumer(
            'notify_events',
            bootstrap_servers='158.160.34.217:9092',
            group_id="my-group-2")
        await consumer.start()
        try:
            async for msg in consumer:
                yield UserCreatedEvent(
                    text="consumed: {} {} {} {} {} {}".format(
                        msg.topic, msg.partition, msg.offset, msg.key,
                        msg.value, msg.timestamp,
                    )
                )
        finally:
            await consumer.stop()
