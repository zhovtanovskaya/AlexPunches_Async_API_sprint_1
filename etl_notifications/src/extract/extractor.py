from typing import AsyncIterable

from extract.models.protocols import Event
from extract.models.user_events import UserCreatedEvent


async def extract(consumer) -> AsyncIterable[Event]:
    async for event in consumer:
        yield event
