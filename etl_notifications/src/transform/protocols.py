from typing import AsyncIterable, Protocol

from extract.models.protocols import Event
from transform.models.protocols import Posting


class Transformer(Protocol):

    async def make_postings(self, event: Event) -> AsyncIterable[Posting]:
        ...
