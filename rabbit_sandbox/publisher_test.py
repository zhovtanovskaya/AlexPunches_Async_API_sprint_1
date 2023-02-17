import asyncio

import aio_pika
import aio_pika.abc
from pydantic import BaseModel


class Notifocation(BaseModel):

    pass


async def main(loop):
    # Explicit type annotation
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
        "amqp://user:123456@158.160.34.217:5672/", loop=loop
    )

    routing_key = "test_queue"

    channel: aio_pika.abc.AbstractChannel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body='Hello 123 {}'.format(routing_key).encode(),
            delivery_mode=2,
        ),
        routing_key=routing_key,
    )

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
