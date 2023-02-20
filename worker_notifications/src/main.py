import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

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
        await channel.set_qos(prefetch_count=config.queue_prefetch_count)

        await channel.declare_exchange(
            config.exchanger_name,
            type=ExchangeType.DIRECT,
            durable=True,
            auto_delete=False,
        )
        await channel.declare_exchange(
            config.retry_exchanger_name,
            type=ExchangeType.DIRECT,
            durable=True,
            auto_delete=False,
        )

        queue = await channel.declare_queue(
            config.queue_name,
            durable=True,
            exclusive=False,
            auto_delete=False,
            arguments={
                'x-max-priority': config.max_priority,
                'x-dead-letter-exchange': config.retry_exchanger_name,
            }
        )
        retry_queue = await channel.declare_queue(
            config.retry_queue_name,
            durable=True,
            exclusive=False,
            auto_delete=False,
            arguments={
                'x-max-priority': config.max_priority,
                'x-dead-letter-exchange': config.exchanger_name,
                'x-message-ttl': config.ttl_for_retry,
            }
        )

        await queue.bind(exchange=config.exchanger_name)
        await retry_queue.bind(exchange=config.retry_exchanger_name)

        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
