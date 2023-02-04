import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.like import LikeService
from src.services.models.user_content import Like, LikeValue
from tests.unit.src.core.config import settings


class TestLikeService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        client = AsyncIOMotorClient(settings.test_mongo_url)
        self.service = LikeService(client.test_ugc)
        self.like = Like(
            user_id='af18023d-9c76-11ed-9485-7831c1bc31e4',
            target_id='63d0c92bf5eb85d9a10bd8ac',
            value=LikeValue.LIKE,
        )

    async def test_create(self):
        new_like = await self.service.create(self.like)
        self.assertIsNotNone(await self.service.get(new_like.id))

    async def test_delete(self):
        new_like = await self.service.create(self.like)
        await self.service.delete(new_like.id)
        self.assertIsNone(await self.service.get(new_like.id))


if __name__ == '__main__':
    unittest.main()