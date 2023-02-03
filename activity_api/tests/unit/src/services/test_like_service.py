import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.like import LikeService
from tests.unit.src.core.config import settings


class TestLikeServiceCreate(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        client = AsyncIOMotorClient(settings.test_mongo_url)
        self.service = LikeService(client.test_ugc)

    async def test(self):
        await self.service.delete('63dd1670e08ddbc85993634c')


if __name__ == '__main__':
    unittest.main()