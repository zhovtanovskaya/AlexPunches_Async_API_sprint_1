from src.consumers.incoming_events import LeadingPlayerChangedEvent
from src.server.consumers import consumer
from src.server.rooms.chat import Room
from src.server.rooms.clients import Client


@consumer()
async def leading_player_changed(client: Client, room: Room, message: dict):
    event = LeadingPlayerChangedEvent(**message)
    await room.send_broadcast(event.model_dump_json())
