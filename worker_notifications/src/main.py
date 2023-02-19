import asyncio
from asyncio import sleep

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.patterns import NackMessage

import senders
from core.config import config, logger
from utils import messages as msg


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        # получить отправлятель
        sender_service = senders.get_sender_by_posting(message.body)

        # проваледировать возможность отправки (часовой пояс и т.п)
        if sender_service.check_permit() is not True:
            await message.nack(requeue=False)

        try:
            sender_service.send()
        except Exception:
            await message.nack(requeue=False)


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
