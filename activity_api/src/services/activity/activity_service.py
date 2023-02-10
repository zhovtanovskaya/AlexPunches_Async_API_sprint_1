"""Ассинхронный сервис для работы с Кафкой."""
import asyncio

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.core.config import config
from src.producer import get_producer
from src.services.activity.models.spawn_point import SpawnPointModel

loop = asyncio.get_event_loop()


class ActivityService:
    """Сервис для работы с хранилищем событий."""

    def __init__(self,
                 producer: AIOKafkaProducer = Depends(get_producer),
                 ):
        """Сервис зависит от Продюсера Кафки."""
        self.producer = producer

    async def send_spawn_point(self, point: SpawnPointModel):
        """Отправить событие в хранилище."""
        key = f'{point.user_id}+{point.film_id}'.encode('utf8')
        value = b'{"time": %d}' % point.time
        await self.producer.send_and_wait(topic=config.film_progress_topic,
                                          value=value,
                                          key=key,
                                          )
