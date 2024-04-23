from src.consumers.incoming_events import SendTextEvent, SetUserNameEvent
from src.consumers.outgoing_events import IncomingTextEvent
from src.server.consumers import consumer


@consumer()
async def help(client, room, message):
    await client.send(', '.join(room.get_client_names()))


@consumer()
async def send_text(client, room, message):
    event = SendTextEvent(**message)
    if event.to == "__all__":
        incoming_text = IncomingTextEvent(text=event.text, author=client.name)
        await room.send_broadcast(incoming_text.model_dump_json())
    elif event.to in room.web_sockets:
        await room.send(event.text, event.to, client.name)
    else:
        await client.send(f'Пользователь {event.to} не найден')

@consumer()
async def set_user_name(client, room, message):
    event = SetUserNameEvent(**message)
    client.name = event.user_name
