from transform.models.protocols import Posting


class Loader:

    async def load(self, posting: Posting):
        ...
