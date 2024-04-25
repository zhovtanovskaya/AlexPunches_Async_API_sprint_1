import unittest

from src.rooms.chat import Room


class TestRoom(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.room = Room()
        self.client = await self.room.register(None)

    def test_get_client_names(self):
        self.assertEqual(self.room.get_client_names(), ['AnonymousClient'])

    def test_leading_client(self):
        self.assertIsNotNone(self.room.leading_client)

    async def test_unregister_client(self):
        await self.room.unregister(self.client)
        self.assertEqual(self.room.get_client_names(), [])
        self.assertIsNone(self.room.leading_client)

    async def test_set_leading_client(self):
        self.assertTrue(self.room.is_leading_client(self.client))
        second_client = await self.room.register(None)
        await self.room.unregister(self.client)
        self.assertTrue(self.room.is_leading_client(second_client))
