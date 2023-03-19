# Простой чат ws://localhost:8765.  Для доступа установить websocat:
# brew install websocat.

import asyncio

import websockets  # Установите этот пакет, если у вас его нет
from orjson import loads
from pydantic import BaseModel
from websockets import WebSocketServerProtocol

# Человек и указатель на его websocket-соединение.
peoples = {}


class Client:
    def __init__(self, ws: WebSocketServerProtocol, name=''):
        self.ws = ws
        self.name = name

    async def send(self, msg):
        await self.ws.send(msg)


class Room:

    def __init__(self):
        self.peoples = {}

    async def register(self, ws: WebSocketServerProtocol):
        # Авторизация и установка статуса ведущий-ведомый. Dependency Inversion.
        await ws.send('Представьтесь!')
        name = await ws.recv()
        await ws.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.')
        await ws.send('Посмотреть список участников можно командой "?"')
        self.peoples[name.strip()] = ws
        return Client(ws, name)

    async def send(self, msg, to, author=None):
        if author:
            # Пересылаем сообщение в канал получателя, указав отправителя
            await self.peoples[to].send(f'Сообщение от {author}: {msg}')
        else:
            await self.peoples[to].send(msg)


class Rooms:
    def __init__(self):
        self.rooms = {}

    def get(self, name: str):
        if name in self.rooms:
            return self.rooms[name]
        else:
            room = Room()
            self.rooms[name] = room
            return room


rooms = Rooms()


class Consumers:
    def __init__(self):
        self.consumers = {}

    def add(self, func, alias: str):
        self.consumers[alias] = func

    def get(self, alias):
        return self.consumers.get(alias, None)


consumers = Consumers()


def consumer(alias: str):
    def func_wrapper(func):
        consumers.add(func, alias)
        return func
    return func_wrapper


@consumer('help')
async def help(client, room, msg):
    await client.send(', '.join(room.peoples.keys()))


@consumer('send_text')
async def send_text(client, room, msg):
    to, text = msg.split(': ', 1)
    if to in room.peoples:
        await room.send(text, to, client.name)
    else:
        await client.send(f'Пользователь {to} не найден')


class Packet(BaseModel):
    type: str
    content: str = ''


async def receiver(ws: websockets.WebSocketServerProtocol, path: str) -> None:
    print('receiver(path)', path, receiver, ws, type(ws))
    await ws.send('Назовите комнату:')
    room_name = await ws.recv()
    room = rooms.get(room_name)
    client = await room.register(ws)
    while True:
        message = (await ws.recv()).strip()
        packet = Packet(**loads(message))
        consumer = consumers.get(packet.type)
        await consumer(client, room, packet.content)


ws_server = websockets.serve(receiver, 'localhost', 8765)
# Запускаем event-loop
loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
