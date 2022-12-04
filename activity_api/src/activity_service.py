"""Ассинхронный сервис для работы с Кафкой."""
import asyncio

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from producer import get_producer

from core.config import config
from models import ActivityModel

loop = asyncio.get_event_loop()


class ActivityService:
    """Сервис для работы с хранилищем событий."""

    def __init__(self,
                 producer: AIOKafkaProducer = Depends(get_producer),
                 ):
        """Сервис зависит от Продюсера Кафки."""
        self.producer = producer

    async def send(self, activity: ActivityModel):
        """Отправить событие в хранилище."""
        key = f'{activity.user_id}+{activity.film_id}'.encode('utf8')
        value = b'%d' % activity.time
        await self.producer.send_and_wait(topic=config.film_progress_topic,
                                          value=value,
                                          key=key,
                                          )
