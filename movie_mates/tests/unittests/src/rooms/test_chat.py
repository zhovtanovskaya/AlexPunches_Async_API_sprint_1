import unittest

from src.rooms.chat import Room


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room = Room()
        self.room.register(None)

    def test_get_client_names(self):
        self.assertEqual(self.room.get_client_names(), ['AnonymousClient'])