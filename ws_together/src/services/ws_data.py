from typing import Any

from core.config import config
from core.ws_protocol import QueryParamProtocol


class WsData:
    """Структура данных, в которой можно быстро получить:

     и спиок всех вебсокетов в руме,
     лида в руме,
     """

    # тут напрашивается сортед сет Редис персистентс
    rooms: dict[str, dict[str, Any]] = {}

    @classmethod
    async def get_websockets_by_room_id(cls, room_id: str) -> set:
        return cls.rooms[room_id]['websockets']

    @classmethod
    async def add_websocket_to_room(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        if room_id not in cls.rooms.keys():
            cls.rooms[room_id] = {}
            cls.rooms[room_id]['websockets'] = {websocket}
            cls.rooms[room_id]['lead'] = websocket
            websocket.roles.add(config.lead_role_name)
        cls.rooms[room_id]['websockets'].add(websocket)
