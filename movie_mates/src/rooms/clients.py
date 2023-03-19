from websockets import WebSocketServerProtocol


class Client:
    def __init__(self, ws: WebSocketServerProtocol, name=''):
        self.ws = ws
        self.name = name

    async def send(self, msg):
        await self.ws.send(msg)
