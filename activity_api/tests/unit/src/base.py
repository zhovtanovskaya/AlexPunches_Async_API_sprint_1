import unittest

from motor.motor_asyncio import AsyncIOMotorClient

from tests.unit.src.core.config import settings


class ReactionTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.db = AsyncIOMotorClient(
            settings.test_mongo_url,
            serverSelectionTimeoutMS=5000,
            tls=bool(settings.mongo_tls_ca_file),
            tlsCAFile=settings.mongo_tls_ca_file,
        )[settings.test_mongo_auth_src]
        await self.db.drop_collection('reactions')
        await self.db.create_collection('reactions')
