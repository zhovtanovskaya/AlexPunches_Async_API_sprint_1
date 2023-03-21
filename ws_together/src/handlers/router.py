import handlers
import orjson

from core.config import config, logger
from core.ws_protocol import QueryParamProtocol
from services.ws_service import get_websocket_service
from utils import messages as msg

HANDLER_MAPPING = {
    config.event_types.broadcast_message: handlers.BroadcastMessageHandler,
    config.event_types.broadcast_command: handlers.BroadcastCommandHandler,
    config.event_types.room_request: handlers.RoomRequestHandler,
}

ws_service = get_websocket_service()


async def message_handler_router(
              websocket: QueryParamProtocol,
              message: str,
) -> None:
    """Роутим сообщение на нужного консюмера.

    Хендлеру сообщение передаем уже в джисоне.
    """
    json_message = orjson.loads(message)
    event_type = json_message.get('event_type')
    type_handler = HANDLER_MAPPING.get(event_type)
    if not type_handler:
        logger.info(msg.unknown_event_type)
        await ws_service.send_error_to_websocket(
            websocket,
            msg.unknown_event_type,
        )
        return None
    handler = type_handler(websocket, json_message)
    await handler.handler()
