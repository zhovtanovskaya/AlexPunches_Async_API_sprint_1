from typing import Any

from core.ws_protocol import QueryParamProtocol
from services.ws_service import get_websocket_service
from utils import messages as msg


class BaseHandler:

    ws_service = get_websocket_service()

    def __init__(self,
                 sender_websocket: QueryParamProtocol,
                 message: dict[str, Any],
                 ):
        self.sender_websocket = sender_websocket
        self.message = message

    def handler(self):
        raise NotImplementedError(msg.def_handler_required)
