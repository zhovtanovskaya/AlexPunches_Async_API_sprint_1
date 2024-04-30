from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from src.server.rooms.clients import Client
from src.server.rooms.outgoing_events import SetLeadingClientEvent

__all__ = ['Room']


class Room:
    """Комната пользователей, общающихся через вебсокеты.

    В комнате есть ведущий клиент.  Состояние плеера ведущего
    клиента транслируется плеерам остальных клиентов в комнате.
    """

    def __init__(self):
        self.clients = set()
        self.leading_client = None        # Ведущий клиент.

    def register(self, ws: WebSocketServerProtocol):
        """Добавить websocket-подключение в комнату."""
        client = Client(ws)
        self.clients.add(client)
        return client

    def unregister(self, client: Client):
        """Удалить клиента из комнаты.

        В случае, если удаляемый клиент являлся ведущим, то
        установить ведущего клиента в `None`.
        """
        try:
            self.clients.remove(client)
        except KeyError:
            pass
        if self.is_leading_client(client):
            self.leading_client = None

    async def set_leading_client(self):
        """Выбрать ведущего клиента.

        Если ведущий клиент уже выбран, то ничего не делать.
        Если ведущего клиента нет, то выбрать его из клиентов в комнате,
        и уведомить его сообщением `SetLeadingClientEvent`.
        """
        if self.leading_client is not None:
            return
        try:
            self.leading_client = self.clients.pop()
        except KeyError:
            # Если подключенных клиентов не осталось.
            self.leading_client = None
        else:
            outgoing_event = SetLeadingClientEvent()
            await self.leading_client.send(outgoing_event.model_dump_json())
            self.clients.add(self.leading_client)

    def is_leading_client(self, client: Client):
        """`True` если `client` равен `self.leading_client`."""
        return client == self.leading_client

    def get_client_names(self) -> list[str]:
        """Получить имена пользователей в комнате."""
        return [c.name for c in self.clients]

    def has_client_name(self, name: str) -> bool:
        return name in self.get_client_names()

    def get_client(self, name: str) -> Client | None:
        """Получить клиета по имени."""
        for client in self.clients:
            if client.name == name:
                return client
        return None

    async def send(self, to: str, message: str):
        """Послать сообщение одному пользователю в комнате."""
        client = self.get_client(to)
        try:
            await client.send(message)
        except ConnectionClosedOK:
            await self.unregister(client)

    async def send_broadcast(self, message: str):
        """Послать сообщение всем пользователям в комнате."""
        failed_clients = []
        for client in self.clients:
            try:
                await client.send(message)
            except ConnectionClosedOK:
                failed_clients.append(client)
        # Удалить из набора клиентов тех, кто отключился.
        # Этого нельзя делать в цикле выше, потому что получается
        # исключение "RuntimeError: Set changed size during iteration".
        for client in failed_clients:
            await self.unregister(client)
