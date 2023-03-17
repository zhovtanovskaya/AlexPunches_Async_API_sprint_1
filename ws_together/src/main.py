import asyncio
import json
import urllib.parse
from http import HTTPStatus
from uuid import UUID

import websockets

USERS = set()


class QueryParamProtocol(websockets.WebSocketServerProtocol):
    """Протокол, в ктором ожидаем два квери параметра:

    token = jwt токен
    room = ид комнаты
    """
    # наверно красивее будет room_id как path, а jwt где-то в заголовках, но это посложнее
    async def process_request(self, path, headers):
        # авторизовать
        token = get_query_param(path, "token")
        if token is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing token\n"
        is_auth = ...
        if is_auth is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Authentication failed\n"

        # проверить доступность рума для юзера
        room = get_query_param(path, "room")
        if room is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing room\n"
        self.room = room


# Какбы вместо однокомнатного USERS = set()
# пока только заготовка
class WsData:
    """Структура данных, в которой можно быстро получить:

     рум по вебсокету,
     и спиок всех вебсокетов в руме."""

    @classmethod
    async def get_all_rooms_websockets_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> set:
        """Получить набор всех вебсокетов, из комнаты websocket'а."""
        room_id = await cls._get_room_id_by_websocket(websocket)
        return await cls._get_websockets_by_room_id(room_id)

    @classmethod
    async def _get_room_id_by_websocket(cls, websocket: QueryParamProtocol) -> str:
        pass

    @classmethod
    async def _get_websockets_by_room_id(cls, room_id: str) -> set:
        return USERS

    @classmethod
    async def add_websocket_to_room(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        USERS.add(websocket)


def create_hello_event() -> dict:
    return {
        'message': 'Добро пожаловать на просмотр фильма вместе!',
        'event_type': 'chat_message',
    }


# в утилиты
def get_query_param(path, key):
    query = urllib.parse.urlparse(path).query
    params = urllib.parse.parse_qs(query)
    values = params.get(key, [])
    if len(values) == 1:
        return values[0]



async def handler(websocket):
    room = websocket.room
    await WsData.add_websocket_to_room(room_id=room, websocket=websocket)

    hello_event = create_hello_event()
    await websocket.send(json.dumps(hello_event))

    async for message in websocket:
        print(websocket.id, room, message)
        event = json.loads(message)
        clients = await WsData.get_all_rooms_websockets_by_websocket(
            websocket=websocket,
        )
        websockets.broadcast(clients, json.dumps(event))


async def main():
    async with websockets.serve(
                handler,
                host='',
                port=8001,
                create_protocol=QueryParamProtocol,
            ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
