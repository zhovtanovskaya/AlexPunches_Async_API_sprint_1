"""Подключение к Реббиту и декларирование очередей с обменниками."""
from typing import Any, Coroutine

from aio_pika import connect
from aio_pika.abc import (AbstractChannel, AbstractConnection, AbstractQueue,
                          ExchangeType)

from src.core.config import settings

rabbitmq: AbstractConnection | None = None


class RabbitPingError(Exception):
    ...


async def get_rabbitmq() -> AbstractConnection | None:
    """Подключиться к Реббиту."""
    global rabbitmq
    rabbitmq = await connect(
        settings.rabbitmq.get_conn_str(),
        timeout=settings.rabbitmq.mq_timeout,
    )
    return rabbitmq


async def get_notification_queue(channel: AbstractChannel) -> AbstractQueue:
    """Получить очередь для нотификаций. Не забыть настроить retry-очередь."""
    await channel.set_qos(
        prefetch_count=settings.rabbitmq.queue_prefetch_count,
    )
    exchange = await channel.declare_exchange(
        settings.rabbitmq.exchanger_name,
        type=ExchangeType.DIRECT,
        durable=True,
        auto_delete=False,
    )
    return exchange


exchange: Coroutine[Any, Any, AbstractQueue] = None


async def get_rabbitmq_exchange():
    return exchange
