import logging

from orjson import JSONDecodeError, loads
from websockets import WebSocketServerProtocol

from src.server.consumers import Consumers
from src.server.events import Event
from src.server.rooms import Rooms
from src.server.urltools import get_room_name

logger = logging.getLogger(__name__)


class Receiver:
    def __init__(self, consumers: Consumers, rooms: Rooms):
        self.consumers = consumers
        self.rooms = rooms

    async def __call__(self, ws: WebSocketServerProtocol, path: str):
        room_name = get_room_name(path)
        room = self.rooms.get(room_name)
        client = room.register(ws)
        while True:
            message = (await ws.recv()).strip()
            try:
                event = Event(**loads(message))
            except JSONDecodeError as e:
                logger.exception(e)
            else:
                consumer = self.consumers.get(event.type)
                await consumer(client, room, event)
