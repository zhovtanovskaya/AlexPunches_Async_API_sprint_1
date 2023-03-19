from src.server.consumers import consumer


@consumer('help')
async def help(client, room, msg):
    await client.send(', '.join(room.web_sockets.keys()))


@consumer('send_text')
async def send_text(client, room, msg):
    to, text = msg.split(': ', 1)
    if to in room.web_sockets:
        await room.send(text, to, client.name)
    else:
        await client.send(f'Пользователь {to} не найден')
