import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from tests.unit.src.core.config import settings


class ReactionTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.db = AsyncIOMotorClient(
            settings.test_mongo_url,
        )[settings.test_mongo_auth_src]
        await self.db.drop_collection('reactions')
        await self.db.create_collection('reactions')
