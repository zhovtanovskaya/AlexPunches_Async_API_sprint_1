import unittest

from src.server.urltools import get_room_name


class TestGetRoomName(unittest.TestCase):

    def test_room_name_is_correct(self):
        room_name = get_room_name('/test_room/')
        self.assertEqual(room_name, 'test_room')

    def test_room_name_is_empty(self):
        room_name = get_room_name('/')
        self.assertEqual(room_name, '')
