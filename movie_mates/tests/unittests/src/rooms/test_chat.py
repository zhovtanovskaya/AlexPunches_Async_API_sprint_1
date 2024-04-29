import unittest

from src.rooms.chat import Room


class TestRoom(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.room = Room()
        self.client = self.room.register(None)
        await self.room.set_leading_client()

    def test_get_client_names(self):
        self.assertEqual(self.room.get_client_names(), ['AnonymousClient'])

    async def test_set_leading_client(self):
        self.assertTrue(self.room.is_leading_client(self.client))

    async def test_unregister_client(self):
        self.room.unregister(self.client)
        self.assertEqual(self.room.get_client_names(), [])
        self.assertIsNone(self.room.leading_client)
