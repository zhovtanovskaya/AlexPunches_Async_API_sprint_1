import asyncio

from extract.extractor import Extractor


async def etl():
    extractor = Extractor()
    async for event in extractor.extract():
        print(event)


if __name__ == '__main__':
    try:
        asyncio.run(etl())
    except KeyboardInterrupt:
        pass
