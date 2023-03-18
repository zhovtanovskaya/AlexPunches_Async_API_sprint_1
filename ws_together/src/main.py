import asyncio

import websockets
from redis import asyncio as aioredis

from core.config import config
from core.ws_protocol import QueryParamProtocol
from db import db_redis
from services.ws_service import get_websocket_service

ws_service = get_websocket_service()


async def handler(websocket):
    room_id = websocket.room_id
    await ws_service.add_websocket_to_room(room_id, websocket)

    # отправить текущий стейт подключившемуся
    state_msg = await ws_service.create_state_by_room_id(room_id)
    await ws_service.send_to_websocket(websocket, message=state_msg)
    # отправить приветственное сообщение
    hello_msg = await ws_service.create_hello_event(websocket)
    await ws_service.send_to_websocket(websocket, message=hello_msg)

    async for message in websocket:
        if not ws_service.validate_message(websocket, message):
            return None
        room_id = await ws_service.get_room_id_by_websocket(websocket)
        await ws_service.broadcast_to_room(room_id, message)


async def main():
    db_redis.redis = await aioredis.Redis(
        host=config.redis_host, port=config.redis_port, db=config.redis_db,
    )
    async with websockets.serve(
                handler,
                host='',
                port=8001,
                create_protocol=QueryParamProtocol,
            ):
        await asyncio.Future()
    await db_redis.redis.close()


if __name__ == "__main__":
    asyncio.run(main())
