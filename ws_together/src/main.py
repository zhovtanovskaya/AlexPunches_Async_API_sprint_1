import asyncio
import json

import websockets
from redis import asyncio as aioredis

from core.config import config
from core.ws_protocol import QueryParamProtocol
from db import db_redis
from services.ws_data import WsData
from services.ws_service import get_websocket_service

ws_service = get_websocket_service()


async def handler(websocket):
    room_id = websocket.room_id
    await WsData.add_websocket_to_room(room_id=room_id, websocket=websocket)

    hello_event = ws_service.create_hello_event(websocket)
    await websocket.send(json.dumps(hello_event))

    async for message in websocket:
        event = json.loads(message)
        clients = await WsData.get_all_rooms_websockets_by_websocket(
            websocket=websocket,
        )
        websockets.broadcast(clients, json.dumps(event))


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
