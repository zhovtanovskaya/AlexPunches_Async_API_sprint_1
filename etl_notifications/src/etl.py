from datetime import datetime

from aio_pika import Message
from aiokafka import AIOKafkaConsumer

from src.db.kafka import get_kafka_consumer
from src.extract.extractor import extract
from src.load.postings.users import UserInfo, WelcomeEmailPosting
from src.mq.rabbitmq import get_rabbitmq_exchange


async def etl():
    consumer: AIOKafkaConsumer = await get_kafka_consumer()
    exchange = await get_rabbitmq_exchange()
    # Sending the message
    user = UserInfo(name='Name', last_name='Last', email='email@mail.com')
    posting = WelcomeEmailPosting(deadline=datetime(2023, 2, 24), user=user)
    message = Message(body=posting.json_bytes())
    await exchange.publish(
        message, routing_key='notifications',
    )
    async for event in extract(consumer):
        print(event)

    # extractor = Extractor(consumer)
    # transformer = Transformer()
    # loader = Loader()
    # async for event in extractor.extract():
    #     print(event)
    #     await transformer.add_event(event)
    #     posting = await transformer.get_posting()
    #     await loader.load(posting)

