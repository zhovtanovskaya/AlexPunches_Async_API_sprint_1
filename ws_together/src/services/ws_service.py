import json
from functools import lru_cache
from typing import Type

import websockets

from core.config import config
from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData
from utils import messages as msg


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
              message: str,
    ) -> None:
        clients = await cls.ws_data.get_websockets_by_room_id(room_id)
        websockets.broadcast(clients, message)

    @classmethod
    def validate_message(
              cls,
              websocket: QueryParamProtocol,
              message: str,
    ) -> bool:
        json_message = json.loads(message)
        event_type = json_message.get('event_type')
        message_text = json_message.get('message')
        if not event_type:
            return False

        if event_type == 'player_command':
            if config.lead_role_name in websocket.roles:
                return True

        if event_type == 'chat_message':
            if config.mute_role_name not in websocket.roles:
                return True

        if event_type == 'room_state':
            if (
                  message_text == 'sent_state' and
                  config.lead_role_name not in websocket.roles
            ):
                # принимаем стейт только от ведущего
                return False
            return True
        return False

    @classmethod
    async def add_websocket_to_room(
              cls,
              room_id: str,
              websocket: QueryParamProtocol,
    ) -> None:
        await cls.ws_data.add_websocket_to_room(room_id, websocket)

    @classmethod
    async def get_room_id_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> str:
        return await cls.ws_data.get_room_id_by_websocket(websocket)

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
    async def create_hello_event(websocket: QueryParamProtocol) -> dict:
        if config.lead_role_name in websocket.roles:
            return {
                'message': 'you_are_leader',
                'event_type': config.event_types.player_command,
            }
        return {
            'message': msg.hello,
            'event_type': config.event_types.chat_message,
        }

    @classmethod
    async def create_state_by_room_id(cls, room_id: str) -> dict:
        return {
            'timecode': 20,
            'player_status': config.player_statuses.play,
            'chat_messages': [
                {
                    'datetime': '',
                    'user_name': 'user_1',
                    'message': 'qwerqwe',
                },
                {
                    'datetime': '',
                    'user_name': 'user_1',
                    'message': '444444444',
                },
            ],
            'event_type': config.event_types.room_state,
        }


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
