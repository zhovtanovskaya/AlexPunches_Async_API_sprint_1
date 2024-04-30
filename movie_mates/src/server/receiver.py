"""Получатель всех сообщений, поступающих в вебсокет."""

import logging

from orjson import JSONDecodeError, loads
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from src.server.consumers import Consumers
from src.server.rooms import Rooms
from src.server.urltools import get_room_name

logger = logging.getLogger(__name__)

__all__ = ['Receiver']


class Receiver:
    """Получатель сообщений из веб-сокета.

    Получает сообщения в виде JSON-строки и передает их на
    обработку соответствующему консьюмеру в виде `dict`.
    """

    def __init__(self, consumers: Consumers, rooms: Rooms):
        self.consumers = consumers
        self.rooms = rooms

    async def __call__(self, ws: WebSocketServerProtocol, path: str):
        """Подключить вебсокет к комнате, указанной в `path`.

        Arguments:
        ws - новый вебсокет в комнате.
        path - URL-путь, в котором указано имя комнаты, например,
        '/test_room/'.
        """
        room_name = get_room_name(path)
        room = self.rooms.get(room_name)
        client = room.register(ws)
        while True:
            try:
                await room.set_leading_client()
                message = (await ws.recv()).strip()
            except (ConnectionClosedOK, ConnectionClosedError):
                room.unregister(client)
                continue
            try:
                message_json = loads(message)
            except JSONDecodeError as e:
                logger.exception(e)
                continue
            consumer = self.consumers.get(message_json['type'])
            if consumer is None:
                logger.info(f'Consumer {consumer} not found.')
                continue
            # Вызвать консьюмера этого типа сообщений, если
            # он найден.
            try:
                await consumer(client, room, message_json)
            except (ConnectionClosedOK, ConnectionClosedError):
                room.unregister(client)