import asyncio

from aio_pika.abc import AbstractIncomingMessage

import senders
import senders.exceptions as sender_exc
from mq.rabbitmq import get_notification_queue, get_rabbitmq


async def on_message(message: AbstractIncomingMessage) -> None:
    """Пытаемся отправить сообщение по нужному каналу."""
    async with message.process():
        sender_service = senders.get_sender_by_posting(message.body)

        try:
            sender_service.send()
        except sender_exc.TimeOfDayNotifyError:
            await message.nack(requeue=False)
        except sender_exc.DeadlineNotifyError:
            return None


async def main() -> None:
    connection = await get_rabbitmq()

    async with connection:
        channel = await connection.channel()
        queue = await get_notification_queue(channel)

        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
