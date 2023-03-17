from functools import lru_cache

from core.config import config
from core.ws_protocol import QueryParamProtocol
from utils import messages as msg


class WebsocketService:

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
