from http import HTTPStatus

import websockets

from utils.helpers import get_query_param, get_room_id_by_path


class QueryParamProtocol(websockets.WebSocketServerProtocol):
    """Протокол,

    в ктором ожидаем квери параметр:
    token = jwt токен
    и path-параметр
    room_id = ид комнаты
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
        room = get_room_id_by_path(path)
        if room is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing room\n"
        self.room = room
