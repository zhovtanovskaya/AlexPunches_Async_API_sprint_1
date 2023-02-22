import unittest

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.extract.extractor import extract
from tests.unit.src.core.config import settings
from tests.unit.src.extract.fixtures.events import UserSignedUpEvent


class ExtractTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.consumer = AIOKafkaConsumer(
            settings.kafka.notifications_topic,
            bootstrap_servers=settings.kafka.bootstrap_servers,
            group_id=settings.kafka.test_notifications_group_id,
        )
        await self.consumer.start()
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka.bootstrap_servers,
        )
        await self.producer.start()
        await self.producer.send_and_wait(
            settings.kafka.notifications_topic,
            UserSignedUpEvent().json().encode(),
        )

    async def asyncTearDown(self):
        await self.consumer.stop()
        await self.producer.stop()

    async def test(self):
        event = await anext(extract(self.consumer))
        self.assertEqual('auth', event.from_service)
