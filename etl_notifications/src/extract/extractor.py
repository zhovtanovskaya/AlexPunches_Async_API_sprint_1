from typing import AsyncIterable

import orjson

from src.extract.events.protocols import Event
from src.extract.events.users import UserSignedUpEvent


async def extract(consumer) -> AsyncIterable[Event]:
    async for event in consumer:
        d = orjson.loads(event.value.decode())
        yield UserSignedUpEvent(**d)
