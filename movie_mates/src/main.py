# Простой чат ws://localhost:8765.  Для доступа установить websocat:
# brew install websocat.

import asyncio

import websockets  # Установите этот пакет, если у вас его нет
from websockets import WebSocketServerProtocol

# Человек и указатель на его websocket-соединение.
peoples = {}


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
        return name

    async def send(self, msg, author, to):
        # Пересылаем сообщение в канал получателя, указав отправителя
        await self.peoples[to].send(f'Сообщение от {author}: {msg}')


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


async def receiver(ws: websockets.WebSocketServerProtocol, path: str) -> None:
    print('receiver(path)', path, receiver, ws)
    await ws.send('Назовите комнату:')
    room_name = await ws.recv()
    room = rooms.get(room_name)
    name = await room.register(ws)
    while True:
        message = (await ws.recv()).strip()
        if message == '?':
            await ws.send(', '.join(room.peoples.keys()))
            continue
        else:
            # Остальные сообщения попытаемся проанализировать
            # и отправить нужному собеседнику
            to, text = message.split(': ', 1)
            if to in room.peoples:
                await room.send(text, name, to)
            else:
                await ws.send(f'Пользователь {to} не найден')


ws_server = websockets.serve(receiver, 'localhost', 8765)
# Запускаем event-loop
loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
