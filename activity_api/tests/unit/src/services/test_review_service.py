import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.review import ReviewService
from tests.unit.src.core.config import settings


class TestLikeService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        client = AsyncIOMotorClient(settings.test_mongo_url)
        self.service = ReviewService(client.test_ugc)

    async def test(self):
        async for review in self.service.get_all():
            print(type(review))
