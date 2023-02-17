import asyncio

from extract.extractor import Extractor
from load.loader import Loader
from transform.transformer import Transformer


async def etl():
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()
    async for event in extractor.extract():
        print(event.text)
        await transformer.add_event(event)
        posting = await transformer.get_posting()
        await loader.load(posting)


if __name__ == '__main__':
    try:
        asyncio.run(etl())
    except KeyboardInterrupt:
        pass
