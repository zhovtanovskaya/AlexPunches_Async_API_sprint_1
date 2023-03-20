import random
from dataclasses import dataclass, field
from functools import lru_cache

from core.config import config
from core.ws_protocol import QueryParamProtocol


@dataclass
class RoomState:
    timecode: float  # sec
    player_status: config.player_statuses
    speed: float = 1.0


@dataclass
class Room:
    id: str
    clients: set[QueryParamProtocol] = field(default_factory=set)
    lead: QueryParamProtocol | None = None
    state: RoomState | None = None


class WsData:
    """Структура данных, в которой можно быстро получить:

     и спиок всех вебсокетов в руме,
     лида в руме,
     """

    rooms: dict[str, Room] = {}

    def get_websockets_by_room_id(
              self,
              room_id: str,
    ) -> set[QueryParamProtocol] | None:
        if room := self.rooms.get(room_id):
            return room.clients
        return None

    def get_lead_by_room_id(self, room_id: str) -> QueryParamProtocol | None:
        if room := self.rooms.get(room_id):
            return room.lead
        return None

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
            self._set_lead_for_room(room_id, websocket)

    async def remove_websocket_from_room(
              self,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        room = self.rooms.get(room_id)
        if room and websocket in room.clients:
            room.clients.remove(websocket)

    def delete_room(self, room_id: str,) -> None:
        room = self.rooms.get(room_id)
        if room and len(room.clients) > 0:
            return None
        self.rooms.pop(room_id)

    def set_random_lead_for_room(self, room_id: str,) -> QueryParamProtocol:
        room = self.rooms.get(room_id)
        if not room:
            return None
        new_lead: QueryParamProtocol = random.choice(list(room.clients))
        self._set_lead_for_room(room_id, new_lead)
        return new_lead

    def set_state_for_room(self, room_id: str, state: RoomState) -> None:
        room = self.rooms.get(room_id)
        if not room:
            return None
        room.state = state

    def get_state_for_room(self, room_id: str) -> RoomState | None:
        if room := self.rooms.get(room_id):
            return room.state
        return None

    def _set_lead_for_room(
              self,
              room_id: str,
              webdocket: QueryParamProtocol,
    ) -> None:
        """Назначить ведущего.

        при этом текущий ведущий больше не ведущий.
        """
        room = self._get_or_create_room_by_id(room_id)
        room.lead = webdocket

    def _get_or_create_room_by_id(self, room_id: str) -> Room:
        if room := self.rooms.get(room_id):
            return room
        self.rooms[room_id] = Room(id=room_id)
        return self.rooms[room_id]


@lru_cache()
def get_ws_data() -> WsData:
    return WsData()
