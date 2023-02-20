"""Ассинхронный сервис для работы с Кафкой."""
import asyncio
from functools import lru_cache

from kafka import KafkaProducer

import services.models.users as service_user_models
from core.config import config, logger
from db.kafka_producer import get_producer
from services.models.events import WelcomUserEventModel
from utils import messages as msg

loop = asyncio.get_event_loop()


class EventService:
    """Сервис для работы с хранилищем событий."""

    def __init__(self, producer: KafkaProducer = get_producer()):
        """Сервис зависит от Продюсера Кафки."""
        self.producer = producer

    def send_event(self, event: WelcomUserEventModel) -> None:
        """Отправить событие в хранилище."""
        if self.producer is None:
            logger.info(msg.event_has_not_been_sent)
            return None
        key = f'{event.id}+{event.event_type}'.encode('utf8')
        value = event.json()
        self.producer.send(
            topic=config.notify_events_topic,
            value=value.encode('utf-8'),
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
