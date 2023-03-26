# import random
from http import HTTPStatus

import websockets

from auth import decode_jwt
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
        # для демонстрации отключить авторизацию
        self.token = get_query_param(path, "token")
        # if self.token is None:
        #     return HTTPStatus.UNAUTHORIZED, [], b"Missing token\n"
        # auth_payload = decode_jwt(self.token)
        # if auth_payload is None:
        #     return HTTPStatus.UNAUTHORIZED, [], b"Authentication failed\n"

        room_id = get_room_id_by_path(path)
        if room_id is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing room\n"
        self.room_id = room_id

        # тут будут разные роли, например mute, и т.д.
        self.roles = set()
        self.user_name = None

    @property
    async def is_organizer(self) -> bool:
        """Сверяемся с системой бронирования."""
        # для демонстрации рандомный ведущий
        # return random.choice([True, False])
        if auth_payload := decode_jwt(self.token):
            return config.admin_role_name in auth_payload.roles
        return False

    def add_role(self, role_name: str) -> None:
        self.roles.add(role_name)

    def remove_role(self, role_name: str) -> None:
        self.roles.remove(role_name)
