import asyncio

import websockets
from handlers.router import message_handler_router

from core.config import logger
from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData, get_ws_data
from services.ws_service import WebsocketService, get_websocket_service

ws_service: WebsocketService = get_websocket_service()
ws_data: WsData = get_ws_data()

async def handler(websocket):
    room_id = websocket.room_id
    await ws_data.add_websocket_to_room(room_id, websocket)
    await ws_service.welcome_websocket(websocket)

    try:
        async for message in websocket:
            await message_handler_router(websocket, message)
    except Exception as e:
        logger.warning(e)
    finally:
        await ws_service.goodbay_websocket(room_id, websocket)


async def main():
    async with websockets.serve(
                handler,
                host='',
                port=8001,
                create_protocol=QueryParamProtocol,
            ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
