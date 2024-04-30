__all__ = ['Rooms']


class Rooms:
    def __init__(self, room_class):
        self.rooms = {}
        self.room_class = room_class

    def get(self, name: str):
        if name in self.rooms:
            return self.rooms[name]
        else:
            room = self.room_class()
            self.rooms[name] = room
            return room
