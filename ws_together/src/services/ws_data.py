from dataclasses import dataclass, field
from functools import lru_cache

from core.config import config
from core.ws_protocol import QueryParamProtocol


@dataclass()
class Room:
    id: str
    clients: set[QueryParamProtocol] = field(default_factory=set)
    lead: QueryParamProtocol | None = None


class WsData:
    """Структура данных, в которой можно быстро получить:

     и спиок всех вебсокетов в руме,
     лида в руме,
     """

    # тут напрашивается сортед сет Редис персистентс
    rooms: dict[str, Room] = {}

    def _get_or_create_room_by_id(self, room_id: str) -> Room:
        if room := self.rooms.get(room_id):
            return room
        self.rooms[room_id] = Room(id=room_id)
        return self.rooms[room_id]

    async def get_websockets_by_room_id(
              self,
              room_id: str,
    ) -> set[QueryParamProtocol]:
        room = self._get_or_create_room_by_id(room_id)
        return room.clients

    async def add_websocket_to_room(
              self,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        """Добавить подключение к руму,

        Если у добавляется ведущи, то назначить его.
        """
        room = self._get_or_create_room_by_id(room_id)
        room.clients.add(websocket)

        if await websocket.is_organizer:
            self.set_lead_for_room(room_id, websocket)

    def set_lead_for_room(
              self,
              room_id: str,
              webdocket: QueryParamProtocol,
    ) -> None:
        """Назначить ведущего.

        при этом текущий ведущий больше не ведущий.
        """
        room = self._get_or_create_room_by_id(room_id)
        room.lead = webdocket

    def get_lead_by_room_id(self, room_id: str) -> QueryParamProtocol | None:
        if room := self.rooms.get(room_id):
            return room.lead
        return None


@lru_cache()
def get_ws_data() -> WsData:
    return WsData()
