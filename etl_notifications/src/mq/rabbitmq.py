"""Подключение к Реббиту и декларирование очередей с обменниками."""
import asyncio
from typing import Any, Coroutine

from aio_pika import connect
from aio_pika.abc import (AbstractChannel, AbstractConnection, AbstractQueue,
                          ExchangeType)
from aiormq import AMQPConnectionError

from src.core.config import settings

# from utils.backoff import backoff

rabbitmq: AbstractConnection | None = None


class RabbitPingError(Exception):
    ...


# @backoff(
#     AMQPConnectionError, asyncio.exceptions.TimeoutError,
#     _logger=logger,
# )
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
