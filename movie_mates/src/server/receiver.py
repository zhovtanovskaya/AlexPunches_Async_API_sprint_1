import websockets
from orjson import loads

from src.server.consumers import Consumers
from src.server.events import Event
from src.server.rooms import Rooms


class Receiver:
    def __init__(self, consumers: Consumers, rooms: Rooms):
        self.consumers = consumers
        self.rooms = rooms

    async def __call__(self, ws: websockets.WebSocketServerProtocol, path: str):
        await ws.send('Назовите комнату:')
        room_name = await ws.recv()
        room = self.rooms.get(room_name)
        client = await room.register(ws)
        while True:
            message = (await ws.recv()).strip()
            event = Event(**loads(message))
            consumer = self.consumers.get(event.type)
            await consumer(client, room, event.content)
