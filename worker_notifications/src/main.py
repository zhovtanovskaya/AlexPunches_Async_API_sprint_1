import asyncio

from aio_pika.abc import AbstractIncomingMessage

import senders
import senders.exceptions as sender_exc
from mq.rabbitmq import get_notification_queue, get_rabbitmq
from senders.pick import get_sender_by_posting


async def on_message(message: AbstractIncomingMessage) -> None:
    """Пытаемся отправить сообщение по нужному каналу."""
    async with message.process():
        posting = WelcomeUserPosting()
        sender_service = get_sender_by_posting(message.body)
        # is_expired()
        if posting.requires_daytime() and not posting.is_daytime():
            await message.nack(requeue=False)
        # is_ready()
        if not posting.is_actual():
            return None
        if not user.is_allowed():
            return None
        sender_service.send()


async def main() -> None:
    connection = await get_rabbitmq()

    async with connection:
        channel = await connection.channel()
        queue = await get_notification_queue(channel)

        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
