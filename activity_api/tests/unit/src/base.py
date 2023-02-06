import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from tests.unit.src.core.config import settings


class ReactionTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        client = AsyncIOMotorClient(settings.test_mongo_url)
        self.db = client.test_ugc
        await self.db.drop_collection('reactions')
        await self.db.create_collection('reactions')
