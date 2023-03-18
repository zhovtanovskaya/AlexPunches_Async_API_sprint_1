import json
from functools import lru_cache

import websockets

from core.config import config
from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData
from utils import messages as msg


class WebsocketService:

    @classmethod
    async def broadcast_to_room(
              cls,
              websocket: QueryParamProtocol,
              message: str,
    ) -> None:
        if not cls._validate_message(websocket, message):
            return None
        clients = await WsData.get_rooms_websockets_by_websocket(websocket)
        websockets.broadcast(clients, message)

    @classmethod
    def _validate_message(
              cls,
              websocket: QueryParamProtocol,
              message: str,
    ) -> bool:
        json_message = json.loads(message)
        event_type = json_message.get('event_type')
        if not event_type:
            return False
        if event_type == 'player_command':
            if config.lead_role_name not in websocket.roles:
                return False
        if event_type == 'chat_message':
            if config.mute_role_name in websocket.roles:
                return False
        return True

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
    def create_hello_event(websocket: QueryParamProtocol) -> dict:
        if config.lead_role_name in websocket.roles:
            return {
                'message': 'you_are_leader',
                'event_type': 'player_command',
            }
        return {
            'message': msg.hello,
            'event_type': 'chat_message',
        }


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
