from handlers.base import BaseHandler

from core.config import config, logger
from services.ws_data import WsData, get_ws_data
from services.ws_service import get_websocket_service
from utils import messages as msg

ws_data: WsData = get_ws_data()


class BroadcastMessageHandler(BaseHandler):

    ws_service = get_websocket_service()

    async def handler(self) -> None:
        print(ws_data.rooms)
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
        return True
