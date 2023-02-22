from typing import AsyncIterable

import orjson
from aiokafka import AIOKafkaConsumer

from src.extract.events.protocols import Event
from src.extract.events.users import UserSignedUpEvent


async def extract(consumer: AIOKafkaConsumer) -> AsyncIterable[Event]:
    async for event in consumer:
        d = orjson.loads(event.value.decode())
        yield UserSignedUpEvent(**d)
