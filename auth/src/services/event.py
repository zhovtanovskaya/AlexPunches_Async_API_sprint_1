"""Cервис для работы с Кафкой."""
from functools import lru_cache

from kafka import KafkaProducer

import services.models.users as service_user_models
from core.config import config, logger
from db.kafka_producer import get_producer
from services.auth.auth import get_comfirm_email_url_by_user
from services.models.events import UserSignedUpEventModel
from services.shortlink import ShortlinkService, get_shortlink_service
from utils import messages as msg

shortlink_service: ShortlinkService = get_shortlink_service()


class EventService:
    """Сервис для работы с хранилищем событий."""

    def __init__(self, producer: KafkaProducer = get_producer()):
        """Сервис зависит от Продюсера Кафки."""
        self.producer = producer

    def send_event(self, event: UserSignedUpEventModel) -> None:
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
    ) -> UserSignedUpEventModel:
        """Создать евент регистрации пользователя из модели пользователя."""
        confirm_link = get_comfirm_email_url_by_user(user)
        short_link = shortlink_service.create_shortlink(longlink=confirm_link)
        return UserSignedUpEventModel(
            id=user.id,
            details={
                'email': user.email,
                'confirm_link': short_link,
            }
        )


@lru_cache()
def get_event_service() -> EventService:
    """Создать и/или вернуть синглтон EventService."""
    return EventService()
