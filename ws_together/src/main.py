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
    await ws_service.welcome_websocket(websocket)


    async for message in websocket:
        # если сообщение прошло валидацию, отправляем всей комнате
        # сервисные сообщения обрабатываются на уровне валидации
        if valid_message := await ws_service.validate_message(websocket, message):
            room_id = await ws_service.get_room_id_by_websocket(websocket)
            await ws_service.broadcast_to_room(room_id, valid_message)


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
