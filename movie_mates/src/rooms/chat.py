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

    def has_client_name(self, name: str) -> bool:
        return name in self.get_client_names()

    def get_client(self, name: str) -> Client:
        for client in self.clients:
            if client.name == name:
                return client

    async def send(self, to: str, message: str):
        client = self.get_client(to)
        await client.ws.send(message)

    async def send_broadcast(self, message: str):
        for ws in self.web_sockets:
            await ws.send(message)