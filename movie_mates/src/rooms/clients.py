from websockets import WebSocketServerProtocol


class Client:
    def __init__(self, ws: WebSocketServerProtocol, name='AnonymousClient'):
        self.ws = ws
        self.name = name

    async def send(self, msg):
        # `self.ws` может быть None в unit-тестах.
        # В других случаях должен быть not None.
        if self.ws is not None:
            await self.ws.send(msg)
