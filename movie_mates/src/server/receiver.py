import logging

from orjson import JSONDecodeError, loads
from websockets import WebSocketServerProtocol

from src.server.consumers import Consumers
from src.server.events import Event
from src.server.rooms import Rooms

logger = logging.getLogger(__name__)


class Receiver:
    def __init__(self, consumers: Consumers, rooms: Rooms):
        self.consumers = consumers
        self.rooms = rooms

    async def __call__(self, ws: WebSocketServerProtocol, path: str):
        await ws.send('Назовите комнату:')
        room_name = await ws.recv()
        room = self.rooms.get(room_name)
        client = await room.register(ws)
        while True:
            message = (await ws.recv()).strip()
            try:
                event = Event(**loads(message))
            except JSONDecodeError as e:
                logger.exception(e)
            else:
                consumer = self.consumers.get(event.type)
                await consumer(client, room, event)
