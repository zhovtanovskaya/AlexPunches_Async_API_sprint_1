from src.server.consumers import consumer


@consumer()
async def help(client, room, event):
    await client.send(', '.join(room.get_client_names()))


@consumer()
async def send_text(client, room, event):
    if event.to in room.web_sockets:
        await room.send(event.content, event.to, client.name)
    else:
        await client.send(f'Пользователь {event.to} не найден')
