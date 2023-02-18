import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from core.config import config, logger
from utils import messages as msg


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(f'\nMessage: {message.body!r}')
        logger.info(msg.message_sent + '\n')


async def main() -> None:
    connection = await connect(config.queue_conn)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            config.queue_name,
            durable=True,
        )

        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
