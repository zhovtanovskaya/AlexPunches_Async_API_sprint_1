from aiokafka import AIOKafkaConsumer

consumer: AIOKafkaConsumer = None


async def get_kafka_consumer() -> AIOKafkaConsumer:
    return consumer
