import asyncio
import json
from uuid import UUID

import websockets

USERS = set()


async def add_user(websocket):
    USERS.add(websocket)


def create_hello_event() -> dict:
    return {
        'message': 'Добро пожаловать на просмотр фильма вместе!',
        'event_type': 'chat_message',
    }

def get_room_users_by_websocket_id(websocket_id: UUID) -> set:
    return USERS


async def handler(websocket):
    auth_message = await websocket.recv()
    await add_user(websocket)

    ## Псевдокод
    auth_message = json.loads(auth_message)
    token = auth_message.get('token')
    is_auth = ...
    if is_auth is None:
        await websocket.close(1011, 'authentication failed')
        return

    hello_event = create_hello_event()
    await websocket.send(json.dumps(hello_event))

    async for message in websocket:
        print(websocket.id, message)
        event = json.loads(message)
        room_users = get_room_users_by_websocket_id(websocket.id)
        websockets.broadcast(room_users, json.dumps(event))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
