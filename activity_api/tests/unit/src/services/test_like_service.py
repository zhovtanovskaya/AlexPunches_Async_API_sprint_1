import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.like import LikeService


class TestLikeServiceCreate(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        mongo_url = "mongodb+srv://yana:vAhgeeoxP8crYvpE@cluster0.ynuujij.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = AsyncIOMotorClient(mongo_url)
        self.service = LikeService(client.test_ugc)

    async def test(self):
        await self.service.delete('63dd0af2e08ddbc859936347')


if __name__ == '__main__':
    unittest.main()