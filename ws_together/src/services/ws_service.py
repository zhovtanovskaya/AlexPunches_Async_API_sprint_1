from functools import lru_cache
from typing import Any

import websockets

from core.config import config
from core.ws_protocol import QueryParamProtocol
from services.models.chat_message import ChatMessagePayload, ChatMessageScheme
from services.models.enums import PlayerType
from services.models.error import ErrorPayload, ErrorScheme
from services.models.transfoms import room_state_to_player_state_scheme
from services.ws_data import WsData, get_ws_data
from utils import messages as msg
from utils.helpers import orjson_dumps


class WebsocketService:

    ws_data: WsData = get_ws_data()

    @classmethod
    async def send_to_websocket(
              cls,
              websocket: QueryParamProtocol,
              message: dict[str, Any],
    ) -> None:
        await websocket.send(orjson_dumps(message))

    @classmethod
    async def broadcast_to_room(
              cls,
              room_id: str,
              message: dict[str, Any],
              exclude: set[QueryParamProtocol] | None = None,
    ) -> None:
        clients = cls.ws_data.get_websockets_by_room_id(room_id)
        if exclude is not None:
            clients = clients - exclude
        websockets.broadcast(clients, orjson_dumps(message))

    @staticmethod
    def assign_role(websocket: QueryParamProtocol, role_name: str) -> None:
        """Добавить роль."""
        websocket.add_role(role_name)

    @staticmethod
    def unassign_role(websocket: QueryParamProtocol,  role_name: str) -> None:
        """Удалить роль."""
        websocket.remove_role(role_name)

    @staticmethod
    async def create_hello_msg() -> ChatMessageScheme:
        return ChatMessageScheme(payload=ChatMessagePayload(
            message=msg.hello,
            from_user=config.chat_bot_name,
        ))

    @classmethod
    async def welcome_websocket(cls, websocket: QueryParamProtocol) -> None:
        """Отправить приветственное сообщение подключившемуся.

        TODO добавить отправку всего чата
        """
        hello_msg = await cls.create_hello_msg()
        await cls.send_to_websocket(
            websocket, message=hello_msg.dict(exclude_none=True))

    @classmethod
    async def goodbay_websocket(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        room_lead = cls.ws_data.get_lead_by_room_id(room_id)
        await cls.ws_data.remove_websocket_from_room(room_id, websocket)

        room_clients = cls.ws_data.get_websockets_by_room_id(room_id)
        if len(room_clients) == 0:
            cls.ws_data.delete_room(room_id)
            return None

        if room_lead == websocket:
            new_lead = cls.ws_data.set_random_lead_for_room(room_id)
            await cls.you_leader(new_lead)

    @classmethod
    async def you_leader(cls, websocket: QueryParamProtocol) -> None:
        room_state = cls.ws_data.get_state_for_room(websocket.room_id)
        message_scheme = room_state_to_player_state_scheme(room_state)
        message_scheme.payload.player_type = PlayerType.lead
        await cls.send_to_websocket(websocket, message=message_scheme.dict())

    @classmethod
    async def send_error_to_websocket(
              cls,
              websocket: QueryParamProtocol,
              message: str,
    ) -> None:
        error_message = ErrorScheme(payload=ErrorPayload(message=message))
        await cls.send_to_websocket(websocket, error_message.dict())


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
