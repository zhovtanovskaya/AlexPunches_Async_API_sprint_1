import asyncio

import websockets

from src.server.consumers import Consumers
from src.server.receiver import Receiver
from src.server.rooms import Rooms
from src.server.rooms.chat import Room


async def main():
    # Создать хэндлер вебсокет-сообщений.
    consumers = Consumers()
    consumers.include(
        'src.consumers.chat',
        'src.consumers.player',
    )
    rooms = Rooms(room_class=Room)
    async with websockets.serve(Receiver(consumers, rooms), 'localhost', 8765):
        await asyncio.Future()      # Run forever.


if __name__ == '__main__':
    asyncio.run(main())
