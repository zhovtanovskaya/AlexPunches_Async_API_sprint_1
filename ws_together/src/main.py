import asyncio
import json

import websockets

from core.ws_protocol import QueryParamProtocol
from services.ws_data import WsData
from services.ws_service import get_websocket_service

ws_service = get_websocket_service()


async def handler(websocket):
    room = websocket.room
    await WsData.add_websocket_to_room(room_id=room, websocket=websocket)

    hello_event = ws_service.create_hello_event()
    await websocket.send(json.dumps(hello_event))

    async for message in websocket:
        event = json.loads(message)
        clients = await WsData.get_all_rooms_websockets_by_websocket(
            websocket=websocket,
        )
        websockets.broadcast(clients, json.dumps(event))


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
