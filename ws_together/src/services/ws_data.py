from core.ws_protocol import QueryParamProtocol
from utils.helpers import get_room_id_by_path


class WsData:
    """Структура данных, в которой можно быстро получить:

     рум по вебсокету,
     и спиок всех вебсокетов в руме."""

    # тут напрашивается сортед сет Редис персистентс
    rooms: dict[str, set] = {}

    @classmethod
    async def get_rooms_websockets_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> set | None:
        """Получить набор всех вебсокетов, из комнаты websocket'а."""
        if room_id := await cls._get_room_id_by_websocket(websocket):
            return await cls._get_websockets_by_room_id(room_id)
        return None

    @classmethod
    async def _get_room_id_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> str | None:
        room_id = get_room_id_by_path(websocket.path)
        if websocket in cls.rooms[room_id]:
            return room_id
        return None

    @classmethod
    async def _get_websockets_by_room_id(cls, room_id: str) -> set:
        return cls.rooms[room_id]

    @classmethod
    async def add_websocket_to_room(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:

        if room_id not in cls.rooms.keys():
            cls.rooms[room_id] = {websocket}
        cls.rooms[room_id].add(websocket)
