from typing import AsyncIterable

from extract.models.protocols import Event
from extract.models.user_events import UserCreatedEvent


class Extractor:

    async def extract(self) -> AsyncIterable[Event]:
        counter = 1
        while counter < 100:
            yield UserCreatedEvent()
            counter += 1
