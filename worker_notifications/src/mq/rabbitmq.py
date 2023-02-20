"""Подключение к Реббиту и декларирование очередей с обменниками."""
from aio_pika import connect
from aio_pika.abc import AbstractChannel, AbstractConnection, ExchangeType
from aiormq import AMQPConnectionError

from core.config import config

rabbitmq: AbstractConnection | None = None


async def get_rabbitmq() -> AbstractConnection | None:
    """Подключиться к Реббиту."""
    global rabbitmq
    if rabbitmq is None:
        try:
            rabbitmq = await connect(config.queue_conn)
        except AMQPConnectionError:
            return None
    return rabbitmq


async def get_notification_queue(channel: AbstractChannel):
    """Получить очередь для нотификаций. Не забыть настроить retry-очередь."""
    await channel.set_qos(
        prefetch_count=config.queue_prefetch_count,
    )

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

    return queue
