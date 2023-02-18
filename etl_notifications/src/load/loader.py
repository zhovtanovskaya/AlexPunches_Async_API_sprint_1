from typing import AsyncIterable

from aio_pika import DeliveryMode, Message, connect
from transform.models.protocols import Posting


class Loader:

    async def load(self, posting: str):
        # Perform connection
        connection = await connect("amqp://user:123456@158.160.34.217:5672/")

        async with connection:
            # Creating a channel
            channel = await connection.channel()
            queue = await channel.declare_queue("task_queue", durable=True)
            message_body = posting.encode('utf8')

            message = Message(
                message_body, delivery_mode=DeliveryMode.PERSISTENT,
            )

            # Sending the message
            await channel.default_exchange.publish(
                message, routing_key=queue.name,
            )

            print(f" [x] Sent {message!r}")
