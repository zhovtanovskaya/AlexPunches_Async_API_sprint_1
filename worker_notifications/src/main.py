import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

import senders
import senders.exceptions as sender_exc
from core.config import config


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        sender_service = senders.get_sender_by_posting(message.body)

        try:
            sender_service.send()
        except sender_exc.TimeOfDayNotifyError:
            await message.nack(requeue=False)
        except sender_exc.DeadlineNotifyError:
            return None


async def main() -> None:
    connection = await connect(config.queue_conn)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            config.queue_name,
            durable=True,
            exclusive=False,
            auto_delete=False,
            arguments={
                'x-max-priority': 10,
            }
        )

        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
