"""Ассинхронный сервис для работы с Кафкой."""
import asyncio

from aiokafka import AIOKafkaProducer
from Async_API_sprint_1.activity_api.src.db.producer import get_producer
from fastapi import Depends

from core.config import config
from models import SpawnPointModel

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
