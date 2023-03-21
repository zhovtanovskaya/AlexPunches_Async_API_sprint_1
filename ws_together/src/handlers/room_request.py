from handlers.base import BaseHandler

from core.config import config, logger
from services.models.enums import PlayerType
from services.models.player_state import PlayerStateScheme
from services.models.transfoms import (player_state_scheme_to_room_state,
                                       room_state_to_player_state_scheme)
from services.ws_data import WsData, get_ws_data
from utils import messages as msg

ws_data: WsData = get_ws_data()


class RoomRequestHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_mapping = {
            config.room_requests.get_chat_state: self.chat_state,
            config.room_requests.get_player_state: self.player_state,
            config.room_requests.set_state: self.set_state,
        }

    async def handler(self) -> None:
        try:
            command = self.message['payload']['command']
        except KeyError:
            return None
        handler = self.handler_mapping.get(command)
        if not handler:
            logger.info(msg.message_not_valid)
            await self.ws_service.send_error_to_websocket(
                self.sender_websocket,
                msg=msg.message_not_valid,
            )
        await handler()

    async def chat_state(self):
        state = await self.ws_service.get_chat_state_by_websocket(
            self.sender_websocket,
        )
        await self.ws_service.send_to_websocket(self.sender_websocket, state)

    async def player_state(self) -> None:
        room_id = self.sender_websocket.room_id
        if room_state := ws_data.get_state_for_room(room_id):
            message_scheme = room_state_to_player_state_scheme(room_state)
        else:
            message_scheme = PlayerStateScheme()
        if self.sender_websocket == ws_data.get_lead_by_room_id(room_id):
            message_scheme.payload.player_type = PlayerType.lead
        await self.ws_service.send_to_websocket(
            self.sender_websocket,
            message_scheme.dict(exclude_none=True),
        )

    async def set_state(self):
        lead = ws_data.get_lead_by_room_id(self.sender_websocket.room_id)
        if self.sender_websocket != lead:
            return None
        state_scheme = PlayerStateScheme(**self.message)
        room_state = player_state_scheme_to_room_state(state_scheme)
        ws_data.set_state_for_room(self.sender_websocket.room_id, room_state)
