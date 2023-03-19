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
    async def validate_message(
              cls,
              websocket: QueryParamProtocol,
              message: str,
    ) -> str | None:
        json_message = json.loads(message)
        event_type = json_message.get('event_type')
        payload = json_message.get('payload')
        if not event_type:
            return None

        if event_type == config.event_types.chat_message:
            if config.mute_role_name not in websocket.roles:
                return message

        if event_type == config.event_types.broadcast_command:
            if config.lead_role_name in websocket.roles:
                return message

        if event_type == config.event_types.room_command:
            room_id = await cls.get_room_id_by_websocket(websocket)
            # get_room_state
            if payload.get('command') == 'get_room_state':
                chat_state = await cls.get_chat_state_by_websocket(room_id)
                await cls.send_to_websocket(websocket, chat_state)
                return None
            # get_player_state
            if payload.get('command') == 'get_player_state':
                player_state = await cls.get_player_state_by_websocket(websocket)
                await cls.send_to_websocket(websocket, player_state)
                return None
            if payload.get('command') == 'set_state':
                if config.lead_role_name not in websocket.roles:
                    # принимаем room_command sent_state только от ведущего
                    return None

            return message
        return None

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
    async def create_hello_msg(websocket: QueryParamProtocol) -> dict:
        return {
            'event_type': config.event_types.chat_message,
            'payload': {
                'message': msg.hello,
                'from': 'bot',
            },
        }

    @classmethod
    async def get_chat_state_by_websocket(
              cls,
              websocket: QueryParamProtocol,
    ) -> dict:
        return {
            'payload': {
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
                'timecode': 20,
            },
            'event_type': config.event_types.player_state,
        }

    @classmethod
    async def welcome_websocket(cls, websocket: QueryParamProtocol) -> None:
        # отправить текущий стейт чата подключившемуся
        chat_state = await cls.get_chat_state_by_websocket(websocket)
        await cls.send_to_websocket(websocket, message=chat_state)
        # # отправить текущий стейт плеера подключившемуся
        # player_state = await cls.get_player_state_by_websocket(websocket)
        # await cls.send_to_websocket(websocket, message=player_state)
        # отправить приветственное сообщение от бота
        hello_msg = await cls.create_hello_msg(websocket)
        await cls.send_to_websocket(websocket, message=hello_msg)


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
