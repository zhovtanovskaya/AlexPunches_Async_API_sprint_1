from typing import AsyncIterable


class Extractor:
    async def extract(self) -> AsyncIterable[int]:
        counter = 1
        while counter < 100:
            yield counter
            counter += 1
