import asyncio

import websockets

from src.rooms.chat import Room
from src.server.consumers import Consumers
from src.server.receiver import Receiver
from src.server.rooms import Rooms

if __name__ == '__main__':
    # Создать сервер.
    consumers = Consumers()
    consumers.include(
        'src.consumers.chat',
        'src.consumers.player',
    )
    rooms = Rooms(room_class=Room)
    ws_server = websockets.serve(Receiver(consumers, rooms), 'localhost', 8765)
    # Запустить event-loop.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
