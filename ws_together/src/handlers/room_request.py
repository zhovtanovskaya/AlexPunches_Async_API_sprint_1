from handlers.base import BaseHandler

from core.config import config, logger
from services.ws_service import get_websocket_service
from utils import messages as msg


class RoomRequestHandler(BaseHandler):

    ws_service = get_websocket_service()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_mapping = {
            config.room_requests.get_room_state: self.room_state,
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

    async def room_state(self):
        state = await self.ws_service.get_room_state_by_websocket(
            self.sender_websocket,
        )
        await self.ws_service.send_to_websocket(self.sender_websocket, state)

    async def player_state(self):
        state = await self.ws_service.get_player_state_by_websocket(
            self.sender_websocket,
        )
        await self.ws_service.send_to_websocket(self.sender_websocket, state)

    async def set_state(self):
        if config.lead_role_name not in self.sender_websocket.roles:
            return None
        # TODO реализовать
        state = self.message
        await self.ws_service.save_state(self.sender_websocket, state)
