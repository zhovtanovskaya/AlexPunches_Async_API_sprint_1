from src.consumers.incoming_events import LeadingPlayerChangedEvent
from src.rooms.chat import Room
from src.rooms.clients import Client
from src.server.consumers import consumer


@consumer()
async def leading_player_changed(client: Client, room: Room, message: dict):
    event = LeadingPlayerChangedEvent(**message)
    await room.send_broadcast(event.model_dump_json())
