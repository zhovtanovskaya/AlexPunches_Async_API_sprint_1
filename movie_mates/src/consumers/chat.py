"""Потребители событий из веб-сокета.

Имена консьюмеров должны быть уникальными на всем сервере.
Консьюмер потребляет события, тип которых в точности
равен названию консьюмера.
"""

from src.consumers.incoming_events import SendTextEvent, SetUserNameEvent
from src.consumers.outgoing_events import (ErrorEvent, IncomingTextEvent,
                                           ListUserNamesEvent)
from src.server.consumers import consumer
from src.server.rooms.chat import Room
from src.server.rooms.clients import Client


@consumer()
async def help(client: Client, room: Room, message: dict):
    """Получить список имен всех участников чата."""
    list_user_names = ListUserNamesEvent(user_names=room.get_client_names())
    await client.send(list_user_names.model_dump_json())


@consumer()
async def send_text(client: Client, room: Room, message: dict):
    """Отправить сообщение в чат конкретному получателю или всем."""
    event = SendTextEvent(**message)
    incoming_text = IncomingTextEvent(text=event.text, author=client.name)
    if event.to == '__all__':
        await room.send_broadcast(incoming_text.model_dump_json())
    elif room.has_client_name(event.to):
        await room.send(event.to, incoming_text.model_dump_json())
    else:
        text = f'Пользователь {event.to} не найден.'
        error = ErrorEvent(text=text, on_event=dict(event))
        await client.send(error.model_dump_json())


@consumer()
async def set_user_name(client: Client, room: Room, message: dict):
    """Установить имя пользователя в чате.

    До установления имени пользователя он в чате он считается
    анонимом.
    """
    event = SetUserNameEvent(**message)
    client.name = event.user_name
