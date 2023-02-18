import asyncio
from asyncio import sleep

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.patterns import NackMessage

from core.config import config, logger
from utils import messages as msg


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        # проваледировать возможность отправки (часовой пояс и т.п)
        # определить в какой отправлятель передать

        # try
        #    # отправка
        # except
        #    # Как вернуть в начало очереди (или в другую очередь?) или ETL-ю
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
