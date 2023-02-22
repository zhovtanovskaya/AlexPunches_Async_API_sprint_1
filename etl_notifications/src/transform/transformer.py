from extract.models.protocols import Event
from transform.models.protocols import Posting


class Transformer:

    async def add_event(self, event: Event):
        ...

    async def get_postings(self) -> Posting:
        ...
