import json
from functools import lru_cache
from typing import Type

import websockets

from core.config import config
from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData
from utils import messages as msg
from utils.helpers import orjson_dumps


class WebsocketService:

    ws_data: Type[WsData] = WsData()

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
        clients = await cls.ws_data.get_websockets_by_room_id(room_id)
        if exclude is not None:
            clients = clients - exclude
        websockets.broadcast(clients, orjson_dumps(message))

    @classmethod
    async def add_websocket_to_room(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        await cls.ws_data.add_websocket_to_room(room_id, websocket)

    @staticmethod
    def assign_lead(websocket: QueryParamProtocol) -> None:
        """Назначить ведущим рума."""
        websocket.roles.append(config.lead_role_name)

    @staticmethod
    def assign_mute(websocket: QueryParamProtocol) -> None:
        """Замьютить."""
        websocket.roles.append(config.mute_role_name)

    @staticmethod
    def unassign_lead(websocket: QueryParamProtocol) -> None:
        """Лишить роли ведущего."""
        websocket.roles.remove(config.lead_role_name)

    @staticmethod
    def unassign_mute(websocket: QueryParamProtocol) -> None:
        """Размьютить."""
        websocket.roles.remove(config.mute_role_name)

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
        if config.lead_role_name in websocket.roles:
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

    async def save_state(
              self,
              websocket: QueryParamProtocol,
              message: dict[str, str],
    ):
        pass

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
