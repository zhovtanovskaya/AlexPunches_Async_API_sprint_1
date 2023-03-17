from http import HTTPStatus
from uuid import UUID

import websockets

from core.config import config
from utils.helpers import get_query_param, get_room_id_by_path


class QueryParamProtocol(websockets.WebSocketServerProtocol):
    """Протокол,

    в ктором ожидаем квери параметр:
    token = jwt токен
    и path-параметр
    room_id = ид комнаты
    """

    async def process_request(self, path, headers):
        self.roles = set()  # lead | mute
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

        # TODO Назначить ведущим при необходимости
        user_id = ...
        if user_is_lead(user_id, room_id):
            self.roles.add(config.lead_role_name)
        pass


# TODO Определять ведущесть
def user_is_lead(user_id: UUID, room_id: str) -> bool:
    return False
