import asyncio

import websockets
from handlers.router import message_handler_router

from core.ws_protocol import QueryParamProtocol
from services.ws_service import get_websocket_service

ws_service = get_websocket_service()


async def handler(websocket):
    room_id = websocket.room_id
    await ws_service.add_websocket_to_room(room_id, websocket)
    await ws_service.welcome_websocket(websocket)

    try:
        async for message in websocket:
                await message_handler_router(websocket, message)
    except Exception as e:
        print(f'except {e}')
    finally:
        # TODO
        # удалить из комнаты
        #
        # если ведущий
        #    переназначить
        #
        # если вообще последний
        #    удалить комнату
        print(f'finaly {websocket}')


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
