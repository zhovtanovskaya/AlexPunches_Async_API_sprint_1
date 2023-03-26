from handlers.base import BaseHandler
from pydantic import ValidationError

from core.config import config, logger
from services.models.chat_message import ChatMessageScheme
from services.ws_data import WsData, get_ws_data
from utils import messages as msg

ws_data: WsData = get_ws_data()


class BroadcastMessageHandler(BaseHandler):

    async def handler(self) -> None:
        if not self.validate():
            logger.info(msg.message_not_valid)
            return None

        await self.ws_service.broadcast_to_room(
            room_id=self.sender_websocket.room_id,
            message=self.message,
        )

    def validate(self):
        if config.mute_role_name in self.sender_websocket.roles:
            return False

        try:
            message_scheme = ChatMessageScheme(**self.message)
        except ValidationError:
            return False
        message_scheme.payload.from_user = self.sender_websocket.user_name
        self.message = message_scheme.dict()
        return True
