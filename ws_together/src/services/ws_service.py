from functools import lru_cache

from utils import messages as msg


class WebsocketService:

    @staticmethod
    def create_hello_event() -> dict:
        return {
            'message': msg.hello,
            'event_type': 'chat_message',
        }


@lru_cache()
def get_websocket_service() -> WebsocketService:
    return WebsocketService()
