"""Ассинхронный сервис для работы с Кафкой."""
import asyncio
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

import services.models.users as service_user_models
from core.config import config
from producer import get_producer
from services.models.events import WelcomUserEventModel

loop = asyncio.get_event_loop()


class EventService:
    """Сервис для работы с хранилищем событий."""

    def __init__(self,
                 producer: AIOKafkaProducer = Depends(get_producer),
                 ):
        """Сервис зависит от Продюсера Кафки."""
        self.producer = producer

    def send_event(self, event: WelcomUserEventModel) -> None:
        """Отправить событие в хранилище."""
        key = f'{event.id}+{event.event_type}'.encode('utf8')
        value = event.json()
        self.producer.send_and_wait(
            topic=config.notify_events_topic,
            value=value,
            key=key,
        )

    @staticmethod
    def create_event_user_register(
        user: service_user_models.UserModel,
    ) -> WelcomUserEventModel:
        """Создать евент регистрации пользователя из модели пользователя."""
        return WelcomUserEventModel(
            id=user.id,
            details={
                'email': user.email
            }
        )


@lru_cache()
def get_event_service() -> EventService:
    """Создать и/или вернуть синглтон EventService."""
    return EventService()
