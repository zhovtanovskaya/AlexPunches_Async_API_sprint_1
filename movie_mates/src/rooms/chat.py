from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from src.rooms.clients import Client
from src.rooms.outgoing_events import SetLeadingClientEvent


class Room:
    """Комната пользователей, общающихся через вебсокеты.

    В комнате есть ведущий клиент.  Состояние плеера ведущего
    клиента транслируется плеерам остальных клиентов в комнате.
    """

    def __init__(self):
        self.clients = set()
        self.leading_client = None        # Ведущий клиент.

    async def register(self, ws: WebSocketServerProtocol):
        """Добавить websocket-подключение в комнату.

        Если ведущий клиент комнаты не выбран, то добавляемый для
        веб-сокета клиент будет назначен ведущим.  И ему будет отправлено
        сообщение "set_leading_client".
        """
        client = Client(ws)
        self.clients.add(client)
        # Выбрать ведущего клиента.
        if self.leading_client is None:
            self.leading_client = client
            outgoing_event = SetLeadingClientEvent()
            await self.leading_client.send(outgoing_event.model_dump_json())
        return client

    async def unregister(self, client: Client):
        """Удалить клиента из комнаты.

        В случае, если удаляемый клиент являлся ведущим, выбрать
        нового ведущего клиента из оставшихся.  И уведомить его
        об этом сообщением "set_leading_client".
        """
        try:
            self.clients.remove(client)
        except KeyError:
            pass
        if self.is_leading_client(client):
            # Выбрать нового ведущего клиента.
            try:
                self.leading_client = self.clients.pop()
            except KeyError:
                # Если подключенных клиентов не осталось.
                self.leading_client = None
            else:
                self.clients.add(self.leading_client)
                outgoing_event = SetLeadingClientEvent()
                await self.leading_client.send(outgoing_event.model_dump_json())

    def is_leading_client(self, client: Client):
        return client == self.leading_client

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
