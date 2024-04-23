from websockets import WebSocketServerProtocol

from src.rooms.clients import Client


class Room:

    def __init__(self):
        self.web_sockets = set()
        self.clients = set()
        self.lead = set()

    def register(self, ws: WebSocketServerProtocol):
        """Добавить websocket-подключение в комнату."""
        self.web_sockets.add(ws)
        client = Client(ws)
        self.clients.add(client)
        return client

    def get_client_names(self) -> list[str]:
        return [c.name for c in self.clients]

    async def send(self, msg, to, author=None):
        if author:
            # Пересылаем сообщение в канал получателя, указав отправителя
            await self.web_sockets[to].send(f'Сообщение от {author}: {msg}')
        else:
            await self.web_sockets[to].send(msg)
