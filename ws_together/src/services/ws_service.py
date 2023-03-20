import json
from functools import lru_cache

import websockets

from core.config import config
from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData, get_ws_data
from utils import messages as msg
from utils.helpers import orjson_dumps


class WebsocketService:

    ws_data: WsData = get_ws_data()

    @classmethod
    async def send_to_websocket(
              cls,
              websocket: QueryParamProtocol,
              message: dict[str, str],
    ) -> None:
        await websocket.send(json.dumps(message))

    @classmethod
    async def broadcast_to_room(
              cls,
              room_id: str,
              message: dict[str, str],
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
    async def create_hello_msg(websocket: QueryParamProtocol) -> dict:
        return {
            'event_type': config.event_types.broadcast_message,
            'payload': {
                'message': msg.hello,
                'from': 'bot',
            },
        }

    @classmethod
    async def get_room_state_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> dict:
        return {
            'payload': {
                'chat_messages': [
                    {
                        'datetime': '',
                        'from': 'user_1',
                        'message': 'qwerqwe',
                    },
                    {
                        'datetime': '',
                        'from': 'user_1',
                        'message': '444444444',
                    },
                ],
            },
            'event_type': config.event_types.chat_state,
        }

    @classmethod
    async def get_player_state_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> dict:
        player_type = ''
        if websocket == cls.ws_data.get_lead_by_room_id(websocket.room_id):
            player_type = config.lead_role_name
        return {
            'payload': {
                'player_type': player_type,
                'timecode': 97,
                'player_status': config.player_statuses.pause,
            },
            'event_type': config.event_types.player_state,
        }

    @classmethod
    async def welcome_websocket(cls, websocket: QueryParamProtocol) -> None:
        # отправить текущий стейт чата подключившемуся
        chat_state = await cls.get_room_state_by_websocket(websocket)
        await cls.send_to_websocket(websocket, message=chat_state)
        # отправить приветственное сообщение от бота
        hello_msg = await cls.create_hello_msg(websocket)
        await cls.send_to_websocket(websocket, message=hello_msg)

    @classmethod
    async def goodbay_websocket(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        room_lead = cls.ws_data.get_lead_by_room_id(room_id)
        await cls.ws_data.remove_websocket_from_room(room_id, websocket)

        if room_lead == websocket:
            new_lead = cls.ws_data.set_random_lead_for_room(room_id)
            await cls.you_leader(new_lead)

        room_clients = cls.ws_data.get_websockets_by_room_id(room_id)
        if len(room_clients) == 0:
            cls.ws_data.delete_room(room_id)

    @classmethod
    async def you_leader(cls, websocket: QueryParamProtocol) -> None:
        if state := cls.ws_data.get_state_for_room(websocket.room_id):
            payload = {
                'player_type': config.lead_role_name,
                'timecode': state.timecode,
                'player_status': state.player_status,
                'speed': state.speed,
            }
        else:
            payload = {
                'player_type': config.lead_role_name,
            }
        message = {
            'payload': payload,
            'event_type': config.event_types.player_state,
        }
        await cls.send_to_websocket(websocket, message=message)

    @classmethod
    async def send_error_to_websocket(
              cls,
              websocket: QueryParamProtocol,
              msg: str,
    ) -> None:
        error_message = {
            'payload': {
                'message': msg,
            },
            'event_type': config.event_types.error,
        }
        await cls.send_to_websocket(websocket, error_message)


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
