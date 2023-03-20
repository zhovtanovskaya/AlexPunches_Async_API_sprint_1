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

    async def process_request(self, path, headers):
        # TODO авторизовать
        token = get_query_param(path, "token")
        if token is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing token\n"
        is_auth = ...
        if is_auth is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Authentication failed\n"

        # TODO проверить доступность рума для юзера
        room_id = get_room_id_by_path(path)
        if room_id is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing room\n"
        self.room_id = room_id

        # тут будут разные роли, например mute, и т.д.
        self.roles = set()

    @property
    async def is_organizer(self) -> bool:
        """Сверяемся с системой бронирования."""
        return True
