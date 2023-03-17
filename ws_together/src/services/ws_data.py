from core.ws_protocol import QueryParamProtocol

# тут напрашивается что-то редисное
USERS = set()


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
