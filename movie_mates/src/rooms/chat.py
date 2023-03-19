from websockets import WebSocketServerProtocol

from src.rooms.clients import Client


class Room:

    def __init__(self):
        self.web_sockets = {}
        self.lead = set()

    async def register(self, ws: WebSocketServerProtocol):
        # Авторизация и установка статуса ведущий-ведомый. Dependency Inversion.
        await ws.send('Представьтесь!')
        name = await ws.recv()
        await ws.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.')
        await ws.send('Посмотреть список участников можно командой "?"')
        self.web_sockets[name.strip()] = ws
        return Client(ws, name)

    async def send(self, msg, to, author=None):
        if author:
            # Пересылаем сообщение в канал получателя, указав отправителя
            await self.web_sockets[to].send(f'Сообщение от {author}: {msg}')
        else:
            await self.web_sockets[to].send(msg)
