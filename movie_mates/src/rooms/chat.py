from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from src.rooms.clients import Client


class Room:
    """Комната пользователей, общающихся через вебсокеты."""

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
        """Получить имена пользователей в комнате."""
        return [c.name for c in self.clients]

    def has_client_name(self, name: str) -> bool:
        return name in self.get_client_names()

    def get_client(self, name: str) -> Client:
        """Получить клиета по имени."""
        for client in self.clients:
            if client.name == name:
                return client

    async def send(self, to: str, message: str):
        """Послать сообщение одному пользователю в комнате."""
        client = self.get_client(to)
        await client.ws.send(message)

    async def send_broadcast(self, message: str):
        """Послать сообщение всем пользователям в комнате."""
        for ws in self.web_sockets:
            try:
                await ws.send(message)
            except ConnectionClosedOK as e:
                ...