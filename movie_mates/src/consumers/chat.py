from src.consumers.incoming_events import SendTextEvent, SetUserNameEvent
from src.consumers.outgoing_events import IncomingTextEvent
from src.server.consumers import consumer


@consumer()
async def help(client, room, message):
    await client.send(', '.join(room.get_client_names()))


@consumer()
async def send_text(client, room, message):
    event = SendTextEvent(**message)
    incoming_text = IncomingTextEvent(text=event.text, author=client.name)
    if event.to == "__all__":
        await room.send_broadcast(incoming_text.model_dump_json())
    elif room.has_client_name(event.to):
        await room.send(event.to, incoming_text.model_dump_json())
    else:
        await client.send(f'Пользователь {event.to} не найден')

@consumer()
async def set_user_name(client, room, message):
    event = SetUserNameEvent(**message)
    client.name = event.user_name
